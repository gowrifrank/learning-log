"""End-to-end audit of one deletion request.

  request -> intent -> identity -> linked resources -> state at audit_at -> policy -> ordered steps

Linking runs once, globally, over every known request (sample + evaluation set), because the activity stream
is shared: an account event can only belong to one workflow, so cases are resolved jointly.
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field

from . import evidence as ev
from .config import DATASET, DEFAULT_CATEGORY, system_for
from .identity import IdentityIndex
from .intent import classify
from .planner import ResourceState, load_rules, plan
from .workflow import WorkflowIndex, phase_error, same_workflow, ts

REQUEST_FILES = ("sample_deletion_requests.csv", "deletion_requests.csv")


@dataclass
class CaseTrace:
    """Everything the agent decided for a case, kept for evaluation reports and debugging."""
    case_id: str
    authorized: bool
    intent_reason: str
    user_id: str | None = None
    llm_intent: dict | None = None
    resources: list = field(default_factory=list)
    notes: list = field(default_factory=list)


VLM_STATE = {
    "present": dict(present=True),
    "absent": dict(present=False),
    "redacted": dict(present=True, pii=False),
    "anonymized": dict(present=True, pii=False, ref=False),
    "flow_enabled": dict(present=True, enabled=True),
    "flow_disabled": dict(present=True, enabled=False),
    "restore_allowed": dict(present=True, restore_allowed=True),
    "restore_blocked": dict(present=True, restore_allowed=False),
    "unknown": dict(present=True),
}


def vlm_observations(file_id: str, file_time: str, data: dict) -> list:
    """Turn the vision model's structured screenshot facts into ordinary observations."""
    out = []
    for rec in data.get("records", []):
        rid = rec["resource_id"].strip()
        if not ev.RESOURCE_RE.fullmatch(rid):
            continue
        ids = {e.lower() for e in rec["emails"]} | {u for u in rec["user_refs"] if ev.USER_RE.fullmatch(u)}
        ids |= {"tel:" + p for p in (ev.norm_phone(x) for x in rec["phones"]) if p}
        facts = dict(VLM_STATE.get(rec["state"], {}))
        if rec["state"] in ("present", "unknown"):
            facts.setdefault("pii", bool(rec["shows_personal_data"]))
        out.append(ev.Obs(file_id, file_time, file_time, rid, system_for(rid) or "", idents=frozenset(ids),
                          source="vlm", **facts))
    return out


class Auditor:
    def __init__(self, ocr=None, llm=None, extra_requests: list[dict] | None = None, workflow: bool = True):
        """ocr/llm: optional engines; workflow=False disables activity-stream linking (used for ablations)."""
        self.ids = IdentityIndex()
        self.rules = load_rules()
        self.llm = llm
        self.use_workflow = workflow
        self.obs, self.coverage, self.texts = ev.load_all(ocr=ocr)
        self.vlm: dict[str, dict] = {}
        if llm is not None:                       # vision model reads every screenshot (cross-check for OCR)
            for row in ev.load_manifest():
                if row["file_path"].lower().endswith(".png"):
                    data = llm.read_screenshot(DATASET / row["file_path"])
                    self.vlm[row["file_id"]] = data
                    self.obs.extend(vlm_observations(row["file_id"], row["captured_at"], data))
        with open(DATASET / "system_activity.csv", encoding="utf-8") as f:
            self.activity = list(csv.DictReader(f))
        self.wf = WorkflowIndex(self.activity)

        self.by_res: dict[str, list] = defaultdict(list)
        self.by_ident: dict[str, set] = defaultdict(set)
        self.obs_by_ident: dict[str, list] = defaultdict(list)
        for o in self.obs:
            self.by_res[o.resource_id].append(o)
            for i in o.idents:
                self.by_ident[i].add(o.resource_id)
                self.obs_by_ident[i].append(o)
        # Catalog links in the activity stream ("Data catalog linked X to <email> and user_N")
        self.catalog_links = defaultdict(set)          # resource -> identifiers
        self.catalog_by_ident = defaultdict(set)       # identifier -> resources (O(1) lookup per key)
        for a in self.activity:
            if a["event_type"] == "LINK_RESOURCE_IDENTITY":
                for i in ev.idents_from([a["details"]]):
                    self.by_ident[i].add(a["resource_id"])
                    self.catalog_links[a["resource_id"]].add(i)
                    self.catalog_by_ident[i].add(a["resource_id"])
        # Business documents and screenshots often name a record by an alias (statement number, file name)
        # that the catalog maps to a resource id: "linked export_1842 (NST-2026-0718-1842) to ...".
        aliases = {}
        for a in self.activity:
            m = re.search(r"(?:linked|confirmed) (\w+) \(([^)]+)\)", a["details"])
            if m and m.group(2) != m.group(1) and not m.group(2).startswith("user_"):
                aliases[m.group(2)] = m.group(1)
        manifest = {r["file_id"]: r["captured_at"] for r in ev.load_manifest()}
        for fid, text in self.texts.items():
            for alias, rid in aliases.items():
                if alias in text and system_for(rid):
                    o = ev.Obs(fid, manifest[fid], manifest[fid], rid, system_for(rid), present=True,
                               idents=frozenset(ev.idents_from([text])), source="doc:alias")
                    self.obs.append(o)
                    self.by_res[rid].append(o)
                    for i in o.idents:
                        self.by_ident[i].add(rid)
                        self.obs_by_ident[i].append(o)
        self.repopulated_by = defaultdict(set)        # downstream resource -> data flows that recreated it
        for a in self.activity:
            m = re.search(r"repopulated downstream resource (\w+)", a["details"])
            if a["event_type"] == "SYNC_RECORD" and m:
                self.repopulated_by[m.group(1)].add(a["resource_id"])
        self.owner_of_ident: dict[str, set] = defaultdict(set)
        for uid, u in self.ids.users.items():
            for k in self.ids.resolve(u["email"]).keys:
                self.owner_of_ident[k].add(uid)

        self.requests = []
        for fn in REQUEST_FILES:
            with open(DATASET / fn, encoding="utf-8") as f:
                self.requests += list(csv.DictReader(f))
        # The dataset's requests are classified in fixed batches (stable cache keys); custom evaluation
        # requests get their own batch, and a custom "twin" replaces its base case for linking.
        self.llm_intent = llm.classify_intents(self.requests) if llm is not None else {}
        if llm is not None and extra_requests:
            self.llm_intent.update(llm.classify_intents(extra_requests))
        replaced = {r.get("_replaces") for r in (extra_requests or [])}
        self.requests = [r for r in self.requests if r["case_id"] not in replaced]
        self.requests += extra_requests or []
        self.links: dict[str, tuple[set, list]] = {}
        self._link_all()

    # -------------------------------------------------------------------------------- intent
    def intent(self, req) -> tuple[bool, str]:
        """Rules decide; the LLM's independent verdict only settles texts where no rule cue fired."""
        ok, why = classify(req["request_text"])
        model = self.llm_intent.get(req["case_id"])
        if model and why.startswith("no deletion request") and model["confidence"] == "high":
            return model["authorizes_deletion"], f"llm: {model['reason']}"
        return ok, why

    # -------------------------------------------------------------------------------- ownership
    def owners(self, rid) -> set:
        out = set()
        for o in self.by_res.get(rid, ()):
            for k in o.idents:
                out |= self.owner_of_ident.get(k, set())
        for k in self.catalog_links.get(rid, ()):
            out |= self.owner_of_ident.get(k, set())
        return out

    def owned_by_other(self, rid, uid) -> bool:
        own = self.owners(rid)
        return bool(own) and uid not in own

    # -------------------------------------------------------------------------------- global linking
    def _evidence_links(self, ident, req) -> set:
        """Resources whose evidence carries one of the person's identifiers.

        A *negative* lookup ("query by your email returned 404 for account_X") only says something about
        account_X when it was run for this request, i.e. after the request was submitted. Earlier negative
        lookups are ignored: they can point at someone else's record.
        """
        linked = set()
        for k in ident.keys:
            for o in self.obs_by_ident.get(k, ()):
                if o.present is False and o.time < req["requested_at"]:
                    continue
                linked.add(o.resource_id)
            linked |= self.catalog_by_ident.get(k, set())
        return {r for r in linked if not self.owned_by_other(r, ident.user_id) or ident.user_id is None}

    def _link_all(self):
        cases = []
        for req in self.requests:
            ok, _ = self.intent(req)
            if not ok:
                continue
            ident = self.ids.resolve(req["email"])
            cases.append((req, ident, self._evidence_links(ident, req)))

        # 1) account event per case: evidence-linked account first, otherwise jointly assigned candidates
        account_event: dict[str, dict] = {}
        taken: set[str] = set()
        pending = []
        for req, ident, linked in cases:
            accts = sorted(r for r in linked if r.startswith("account_"))
            evs = [e for e in (self.wf.account_event_for(a, req) for a in accts) if e]
            if evs:
                account_event[req["case_id"]] = evs[0]
                taken |= {e["activity_id"] for e in evs}
            elif not accts and self.use_workflow:
                pending.append((req, ident, linked))

        def score(cand, linked):
            t0 = ts(cand["event_time"])
            return sum(1 for r in linked for e in self.wf.events_by_res.get(r, ())
                       if same_workflow(t0, ts(e["event_time"])))

        options = {}
        for req, ident, linked in pending:
            cands = [c for c in self.wf.account_candidates(req)
                     if c["activity_id"] not in taken and not self.owned_by_other(c["resource_id"], ident.user_id)]
            options[req["case_id"]] = sorted(((score(c, linked), c) for c in cands),
                                             key=lambda x: (-x[0], x[1]["event_time"]))
        # resolve the most constrained cases first; an event can only serve one workflow
        while options:
            cid = min(options, key=lambda k: (len([o for o in options[k] if o[1]["activity_id"] not in taken]),
                                              -max([o[0] for o in options[k]] or [0]), k))
            free = [o for o in options.pop(cid) if o[1]["activity_id"] not in taken]
            if free:
                best = free[0][1]
                account_event[cid] = best
                taken.add(best["activity_id"])

        # 2) every other step of the same workflow (fingerprinted by its seconds-phase)
        claims = defaultdict(list)
        for req, ident, linked in cases:
            a = account_event.get(req["case_id"])
            if not a or not self.use_workflow:
                continue
            t0 = ts(a["event_time"])
            for e in self.wf.chain_events(a):
                claims[e["activity_id"]].append((phase_error(t0, ts(e["event_time"])), req["case_id"], e))
        chain = defaultdict(set)
        for aid, lst in claims.items():
            lst.sort(key=lambda x: x[0])
            if len(lst) == 1 or lst[0][0] < lst[1][0]:      # the closest fingerprint wins; exact ties stay unlinked
                _, cid, e = lst[0]
                chain[cid].add(e["resource_id"])

        for req, ident, linked in cases:
            cid = req["case_id"]
            notes = []
            res = set(linked)
            a = account_event.get(cid)
            if a and a["resource_id"] not in res:
                res.add(a["resource_id"])
                notes.append(f"{a['resource_id']} linked from deletion-workflow account event {a['activity_id']}")
            for r in sorted(chain.get(cid, ())):
                if r not in res and not self.owned_by_other(r, ident.user_id):
                    res.add(r)
                    notes.append(f"{r} linked as a step of the same deletion workflow")
            for r in list(res):
                for flow in self.repopulated_by.get(r, ()):
                    if flow not in res and not self.owned_by_other(flow, ident.user_id):
                        res.add(flow)
                        notes.append(f"{flow} linked: it repopulated {r}")
            self.links[cid] = (res, notes)

    # -------------------------------------------------------------------------------- state
    def state_at(self, rid, audit_at, primary_accounts) -> ResourceState:
        system = system_for(rid) or ""
        obs = [o for o in self.by_res.get(rid, ()) if o.file_time <= audit_at and o.time <= audit_at]
        cats = [o.category for o in self.by_res.get(rid, ()) if o.category and o.category in self.rules]
        category = max(sorted(set(cats)), key=cats.count) if cats else DEFAULT_CATEGORY.get(system, "")
        if system == "integration_service":
            category = "DATA_FLOW"
        if system == "backup_service":
            category = "BACKUP_ARCHIVE"
        # Absence from a full table capture is weaker than an explicit observation, so it is only used
        # when no evidence speaks about the record directly. It can only prove a deletion: a retained,
        # redacted or anonymized record missing from a partial replica table is not evidence of anything.
        deletable = self.rules.get(category, "") == "DELETE"
        if deletable and not any(o.present is not None for o in obs):
            for cov in self.coverage:
                if cov.kind not in ("topology", "bundle") or cov.file_time > audit_at:
                    continue
                if system in cov.present and rid not in cov.present[system]:
                    when = cov.times.get(system, cov.file_time)
                    if when <= audit_at:
                        obs.append(ev.Obs(cov.file_id, cov.file_time, when, rid, system, present=False,
                                          source="sql:absent"))
        # newest first; at equal time the vision model's reading outranks heuristic OCR state words
        obs.sort(key=lambda o: (o.time, o.file_time, o.source == "vlm"), reverse=True)

        def latest(attr):
            return next((o for o in obs if getattr(o, attr) is not None), None)

        rs = ResourceState(rid, system, category, None, None, None, None, None, "",
                           is_primary_account=rid in primary_accounts)
        p = latest("present")
        if p:
            rs.present, rs.evidence_id = p.present, p.file_id
        if category == "DATA_FLOW":
            e = latest("enabled")
            if e:
                rs.enabled, rs.evidence_id = e.enabled, e.file_id
        elif category == "BACKUP_ARCHIVE":
            r = latest("restore_allowed")
            if r:
                rs.restore_allowed, rs.evidence_id = r.restore_allowed, r.file_id
        elif rs.present:
            q = next((o for o in obs if o.pii is not None or o.present is False), None)
            if q and q.present is not False:
                rs.pii, rs.ref, rs.evidence_id = q.pii, q.ref, q.file_id
        return rs

    # -------------------------------------------------------------------------------- case
    def audit(self, req) -> tuple[str, list, CaseTrace]:
        if all(r["case_id"] != req["case_id"] for r in self.requests):   # unseen request (e.g. custom eval case)
            self.requests.append(req)
            if self.llm is not None:
                self.llm_intent.update(self.llm.classify_intents([req]))
            self._link_all()
        ok, why = self.intent(req)
        tr = CaseTrace(req["case_id"], ok, why, llm_intent=self.llm_intent.get(req["case_id"]))
        if not ok:
            return "NOT_APPLICABLE", [], tr
        ident = self.ids.resolve(req["email"])
        tr.user_id = ident.user_id
        linked, notes = self.links[req["case_id"]]
        tr.notes += notes
        accounts = {r for r in linked if r.startswith("account_")}
        states = [self.state_at(r, req["audit_at"], accounts) for r in sorted(linked)]
        tr.resources = states
        status, steps = plan(states, self.rules)
        return status, steps, tr
