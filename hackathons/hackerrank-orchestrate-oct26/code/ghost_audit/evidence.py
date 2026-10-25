"""Evidence readers.

Every evidence file (SQL snapshot, JSON export, log, text handover, PDF, screenshot) is turned into the
same shape: a list of `Obs` objects saying "resource R was seen at time T in this state, carrying these
identifiers". Later stages never look at file formats again; they only reason over observations.
"""
from __future__ import annotations

import csv
import json
import re
import sqlite3
from dataclasses import dataclass, field

from .config import DATASET, DEFAULT_CATEGORY, system_for

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
USER_RE = re.compile(r"\buser_\d+\b")
HASH_RE = re.compile(r"\b[0-9a-f]{64}\b")
RESOURCE_RE = re.compile(
    r"\b(?:audit_record|data_flow|email_delivery|legal_hold|tombstone|analytics|marketing|account|support|search|backup|export|cache)_\d+\b")

# Field names that hold direct identifiers (their presence = personal data still exposed).
DIRECT_KEYS = {"email", "phone", "full_name", "display_name", "name", "email_hash", "requester_email",
               "requester_name", "requester_phone", "owner_email", "owner_phone", "customer_email",
               "matched_value", "uploaded_by", "lookup_value", "subject_selector"}
REF_KEYS = {"customer_reference", "user_id", "subject_reference", "subject_ref", "correlation_key"}
FREE_TEXT_KEYS = {"message_text", "message_excerpt"}
NULLS = {None, "", "null", "none", "None", "NULL", "[REDACTED]", "redacted", "-", "—"}


@dataclass
class Obs:
    file_id: str
    file_time: str                 # manifest captured_at of the evidence file
    time: str                      # when this specific observation was made
    resource_id: str
    system: str
    present: bool | None = None
    pii: bool | None = None        # direct identifiers (name/email/phone/hash/free text) still present
    ref: bool | None = None        # stable user reference (user_123) still present
    enabled: bool | None = None    # data flows
    restore_allowed: bool | None = None  # backups
    category: str | None = None
    idents: frozenset = frozenset()
    source: str = ""               # where in the file it came from (table, collection, event)


def norm_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    return digits if len(digits) >= 7 else ""


def idents_from(values) -> set[str]:
    """Pull every identifier we can link on out of arbitrary strings: emails, user refs, hashes, phones."""
    out: set[str] = set()
    for v in values:
        if not isinstance(v, str) or v in NULLS:
            continue
        out.update(e.lower() for e in EMAIL_RE.findall(v))
        out.update(USER_RE.findall(v))
        out.update(HASH_RE.findall(v.lower()))
        if re.fullmatch(r"[+\d][\d\s()+.-]{6,}", v.strip()):
            p = norm_phone(v)
            if p:
                out.add("tel:" + p)
    return out


def flatten(d, prefix="") -> dict:
    flat = {}
    for k, v in (d or {}).items():
        if isinstance(v, dict):
            flat.update(flatten(v, ""))
        else:
            flat[k] = v
    return flat


def truthy(v) -> bool | None:
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    if s in ("true", "1", "yes", "y", "enabled", "allowed", "active", "on"):
        return True
    if s in ("false", "0", "no", "n", "disabled", "blocked", "denied", "off"):
        return False
    return None


def record_facts(fields: dict) -> dict:
    """Decide pii/ref presence for a flat record of fields."""
    pii = False
    ref = False
    for k, v in fields.items():
        if isinstance(v, (dict, list)) or v in NULLS:
            continue
        k = k.lower()
        if k in DIRECT_KEYS:
            pii = True
        elif k in REF_KEYS and USER_RE.search(str(v)):
            ref = True
        elif k in REF_KEYS and (EMAIL_RE.search(str(v)) or HASH_RE.search(str(v).lower())):
            pii = True
        elif k in FREE_TEXT_KEYS and (EMAIL_RE.search(str(v)) or re.search(r"\+\d[\d\s()-]{7,}", str(v))):
            pii = True
    return {"pii": pii, "ref": ref}


# ---------------------------------------------------------------------------------------------- canonical
CANON_RESULT = {
    "FOUND": dict(present=True),
    "NOT_FOUND": dict(present=False),
    "IDENTIFIABLE": dict(present=True, pii=True),
    "ANONYMIZED": dict(present=True, pii=False, ref=False),
    "REDACTED": dict(present=True, pii=False),
    "ACTIVE": dict(present=True),          # meaning depends on record type (flow enabled / restore allowed)
    "DISABLED": dict(present=True, enabled=False),
    "BLOCKED": dict(present=True, restore_allowed=False),
}


def canonical_obs(file_id, file_time, time, system, resource_id, record_type, result, subject, source):
    """Rows of the shape (system, resource_id, record_type, result, subject_reference)."""
    result = (result or "").strip().upper()
    facts = dict(CANON_RESULT.get(result, {}))
    if result == "ACTIVE" and record_type == "DATA_FLOW":
        facts["enabled"] = True
    if result == "ACTIVE" and record_type == "BACKUP_ARCHIVE":
        facts["restore_allowed"] = True
    if result == "FOUND" and record_type in ("SUPPORT_MESSAGE", "ACCOUNT_TOMBSTONE", "EMAIL_DELIVERY_LOG"):
        facts["pii"] = True   # a found redact-category record listed against a person's identifier
    subj = subject or ""
    ids = idents_from([subj]) if result not in ("ANONYMIZED",) else set()
    category = record_type if record_type in DEFAULT_CATEGORY.values() or record_type else None
    if category == "DATA_FLOW":
        category = "DATA_FLOW"
    return Obs(file_id, file_time, time, resource_id, system or system_for(resource_id) or "",
               category=category, idents=frozenset(ids), source=source, **facts)


# ---------------------------------------------------------------------------------------------- generic record
COLLECTION_CATEGORY = {
    "ticket_attachments": "SUPPORT_ATTACHMENT",
    "support_conversations": "SUPPORT_MESSAGE",
    "deleted_customer_references": "ACCOUNT_TOMBSTONE",
    "retained_order_records": "LEGAL_HOLD_RECORD",
}


def record_obs(file_id, file_time, time, rec: dict, system: str | None, source: str, category=None):
    """A full stored record (SQL row, JSON snapshot record). Present by definition."""
    flat = flatten(rec)
    rid = str(flat.get("resource_id") or "")
    if not rid:
        return None
    if "canonical" in source or ("result" in flat and "record_type" in flat):
        return canonical_obs(file_id, file_time, flat.get("recorded_at") or time, flat.get("system"), rid,
                             flat.get("record_type"), flat.get("result"),
                             flat.get("subject_reference") or flat.get("lookup_value"), source)
    system = system_for(rid) or system or ""
    facts = record_facts(flat)
    o = Obs(file_id, file_time, time, rid, system, present=True, pii=facts["pii"], ref=facts["ref"],
            category=category, idents=frozenset(idents_from(flat.values())), source=source)
    if "enabled" in flat:
        o.enabled = truthy(flat["enabled"])
    if "restore_allowed" in flat:
        o.restore_allowed = truthy(flat["restore_allowed"])
    status = str(flat.get("account_status") or "").upper()
    if system == "account_service" and status in ("DELETED", "CLOSED"):
        o.present = False
    if "download_available" in flat and truthy(flat["download_available"]) is False:
        o.present = False
    return o


# ---------------------------------------------------------------------------------------------- SQL
SQL_TABLE_SYSTEM = {
    "customer_profiles": "account_service",
    "customer_search_documents": "search_service",
    "search_documents": "search_service",
    "customer_analytics_profiles": "analytics_platform",
    "support_records": "support_platform",
    "customer_exports": "export_service",
    "connector_subscriptions": "integration_service",
    "backup_restore_entries": "backup_service",
    "security_audit_records": "security_service",
}


@dataclass
class SqlCoverage:
    """Which systems a SQL snapshot fully lists, so absence from it is meaningful."""
    file_id: str
    file_time: str
    kind: str = "inventory"                        # "topology" = full primary/replica table captures
    times: dict = field(default_factory=dict)      # system -> captured_at
    present: dict = field(default_factory=dict)    # system -> set(resource_id) across ALL tables in the file


def parse_sql(path, file_id, file_time):
    con = sqlite3.connect(":memory:")
    con.executescript(path.read_text(encoding="utf-8"))
    con.row_factory = sqlite3.Row
    tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
    scope = {}
    if "snapshot_scope" in tables:
        scope = {r["origin_system"]: r["captured_at"] for r in con.execute("select * from snapshot_scope")}
    cov = SqlCoverage(file_id, file_time)
    if "Database topology:" in path.read_text(encoding="utf-8")[:600]:
        cov.kind = "topology"
    obs = []
    for t in tables:
        if t == "snapshot_scope":
            continue
        rows = [dict(r) for r in con.execute(f'select * from "{t}"')]
        base = next((k for k in SQL_TABLE_SYSTEM if t.startswith(k)), None)
        label = f"sql:{t}"
        if base:
            system = SQL_TABLE_SYSTEM[base]
            when = scope.get(system, file_time)
            cov.times.setdefault(system, when)
            cov.present.setdefault(system, set())
            for r in rows:
                o = record_obs(file_id, file_time, when, r, system, label)
                if o:
                    cov.present[system].add(o.resource_id)
                    obs.append(o)
        elif "record_json" in (rows[0] if rows else {}) or t.startswith("customer_data"):
            for r in rows:
                rec = json.loads(r["record_json"])
                rec.setdefault("resource_id", r["resource_id"])
                system = r.get("origin_system") or system_for(r["resource_id"])
                when = scope.get(system, file_time)
                cat = COLLECTION_CATEGORY.get(r.get("collection_name") or "")
                o = record_obs(file_id, file_time, when, rec, system, label, cat)
                if o:
                    cov.times.setdefault(o.system, when)
                    cov.present.setdefault(o.system, set()).add(o.resource_id)
                    obs.append(o)
    con.close()
    return obs, cov


# ---------------------------------------------------------------------------------------------- JSON
def parse_json(path, file_id, file_time, coverage=None):
    d = json.loads(path.read_text(encoding="utf-8"))
    obs = []
    if "snapshots" in d:                                   # records-assurance snapshot bundles
        for snap in d["snapshots"]:
            cat = COLLECTION_CATEGORY.get(snap.get("collection", ""))
            if coverage is not None and snap.get("data_store") == "account_service":
                cov = SqlCoverage(file_id, file_time, kind="bundle")
                cov.times["account_service"] = snap["captured_at"]
                cov.present["account_service"] = {r.get("resource_id") for r in snap["records"]}
                coverage.append(cov)
            for rec in snap["records"]:
                o = record_obs(file_id, file_time, snap["captured_at"], rec, snap.get("data_store"),
                               f"bundle:{snap.get('data_store')}/{snap.get('collection')}", cat)
                if o:
                    obs.append(o)
    elif "service_exports" in d:                           # live service read-backs
        for system, lists in d["service_exports"].items():
            for listname, items in lists.items():
                for it in items:
                    obs.extend(service_export_obs(file_id, file_time, system, listname, it))
    elif "records" in d:
        time = d.get("captured_at") or d.get("exported_at") or file_time
        cat = COLLECTION_CATEGORY.get(d.get("collection", ""))
        for rec in d["records"]:
            o = record_obs(file_id, file_time, rec.get("recorded_at") or time, rec, None,
                           f"json:{d.get('collection') or d.get('origin')}", cat)
            if o:
                obs.append(o)
    return obs


def service_export_obs(file_id, file_time, system, listname, it):
    rid = it.get("resource_id")
    t = it.get("observed_at") or file_time
    src = f"export:{system}/{listname}"
    if listname == "profile_lookups":
        prof = it.get("profile")
        found = it.get("status_code") == 200 and prof is not None
        facts = record_facts(prof or {})
        return [Obs(file_id, file_time, t, rid, system, present=found, pii=facts["pii"] if found else None,
                    ref=facts["ref"] if found else None, idents=frozenset(idents_from(flatten(prof or {}).values())),
                    source=src)]
    if listname == "index_queries":
        docs = (it.get("hits") or {}).get("documents") or []
        out = []
        query_ids = idents_from([it.get("query")])
        if not docs:
            out.append(Obs(file_id, file_time, t, rid, system, present=False, idents=frozenset(query_ids), source=src))
        for doc in docs:
            facts = record_facts(doc)
            out.append(Obs(file_id, file_time, t, doc.get("resource_id") or rid, system, present=True,
                           pii=facts["pii"], ref=facts["ref"],
                           idents=frozenset(idents_from(doc.values()) | query_ids), source=src))
        return out
    o = record_obs(file_id, file_time, t, it, system, src)
    return [o] if o else []


# ---------------------------------------------------------------------------------------------- TXT handover
def parse_txt(path, file_id, file_time):
    obs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = [p.strip() for p in line.lstrip("- ").split("|")]
        if len(parts) == 6 and RESOURCE_RE.fullmatch(parts[2]):
            t, system, rid, rtype, result, subj = parts
            obs.append(canonical_obs(file_id, file_time, t, system, rid, rtype, result, subj, "txt:handover"))
    return obs


# ---------------------------------------------------------------------------------------------- logs
KV_RE = re.compile(r'(\w+)=("((?:[^"\\]|\\.)*)"|[^\s"]+)')
STARTED_KEYS = ("lookup_key", "match_key", "subject_key", "owner_key", "subject_ref")


def parse_log_line(line: str) -> dict | None:
    line = line.strip()
    m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+(.*)", line)
    if not m:
        return None
    ts, rest = m.groups()
    ev: dict = {"ts": ts}
    if rest.startswith("{"):                                   # JSON lines
        try:
            ev.update(json.loads(rest))
        except json.JSONDecodeError:
            return None
    else:
        b = re.match(r"\[(\w+)\]\s+\[([\w-]+)\]\s+\[([\w-]+)\]\s+(\w+):\s*(.*)", rest)   # bracket style
        p = rest.split(" | ")                                                           # pipe style
        if b:
            ev.update(level=b.group(1), service=b.group(2), trace_id=b.group(3), event=b.group(4))
            rest = b.group(5)
        elif len(p) >= 5:
            ev.update(level=p[0], service=p[1], trace_id=p[2], event=p[3])
            rest = " | ".join(p[4:])
        else:
            s = re.match(r"<\d+>\d+\s+\S+\s+(\w+)\s+([\w-]+)\s+-\s+-\s+(.*)", rest)       # syslog style
            if s:
                ev.update(service=s.group(1), trace_id=s.group(2))
                rest = s.group(3)
        for k, full, quoted in KV_RE.findall(rest):
            v = quoted.replace('\\"', '"') if full.startswith('"') else full
            ev.setdefault(k, v)
        if "message" in ev and "=" in str(ev["message"]):                              # cloud runtime: nested
            for k, full, quoted in KV_RE.findall(ev["message"]):
                ev.setdefault(k, quoted if full.startswith('"') else full)
    ev.setdefault("service", ev.get("function") or ev.get("logger") or "")
    ev.setdefault("trace_id", ev.get("requestId") or "")
    return ev


def num(v):
    try:
        return int(str(v))
    except (TypeError, ValueError):
        return None


def log_event_obs(ev: dict, trace_ids: set, file_id, file_time):
    rid = ev.get("resource_id")
    name = ev.get("event", "")
    if not rid or not RESOURCE_RE.fullmatch(str(rid)):
        return None
    system = system_for(rid) or ev.get("service")
    t = ev["ts"]
    own = idents_from([v for k, v in ev.items() if k not in ("ts", "trace_id", "requestId", "resource_id")])
    idents = frozenset(own | trace_ids)
    o = Obs(file_id, file_time, t, rid, system, idents=idents, source=f"log:{name}")
    rows = num(ev.get("rows"))
    http = num(ev.get("http_status"))
    if name == "record_lookup":
        return canonical_obs(file_id, file_time, t, ev.get("system"), rid, ev.get("record_type"),
                             ev.get("result"), ev.get("subject_reference"), "log:record_lookup")
    if name in ("profile_lookup_completed",):
        o.present = (rows or 0) > 0 or http == 200
    elif name == "index_query_completed":
        o.present = str(ev.get("result", "")).lower() == "hit"
    elif name in ("audit_record_read_completed", "contact_query_completed"):
        o.present = (rows or 0) > 0
        if name == "contact_query_completed":
            o.category = "SECONDARY_IDENTIFIER"
    elif name == "contact_lookup_completed":
        o.present = (rows or 0) > 0
        o.pii = True
        o.category = "MARKETING_PROFILE"
    elif name in ("connector_config_read_completed", "connector_config_loaded", "connector_heartbeat"):
        o.present = True
        o.enabled = truthy(ev.get("enabled"))
    elif name in ("analytics_profile_read_completed", "analytics_profile_read", "analytics_identity_scan",
                  "support_ticket_read_completed", "message_read"):
        f = {k: v for k, v in ev.items() if k in DIRECT_KEYS | REF_KEYS | FREE_TEXT_KEYS}
        facts = record_facts(f)
        di = num(ev.get("direct_identifiers"))
        o.present = True
        o.pii = facts["pii"] or bool(di)
        o.ref = facts["ref"]
    elif name in ("message_pii_scan", "attachment_pii_scan"):
        o.present = True
        o.pii = True
        o.category = "SUPPORT_ATTACHMENT" if name == "attachment_pii_scan" else "SUPPORT_MESSAGE"
    elif name == "restore_policy_read_completed":
        o.present = truthy(ev.get("archive_present")) is not False
        o.restore_allowed = truthy(ev.get("restore_allowed"))
    elif name == "restore_candidate_evaluated":
        o.present = True
        o.restore_allowed = truthy(ev.get("eligible")) is True and truthy(ev.get("deletion_block")) is not True
    elif name == "restore_authorization_completed":
        o.present = True
        o.restore_allowed = str(ev.get("decision", "")).lower() in ("allow", "allowed", "approve", "approved", "permit")
    elif name in ("export_metadata_read_completed", "export_download_check_completed"):
        o.present = truthy(ev.get("available")) is not False
    elif name == "deletion_marker_check":
        o.present = truthy(ev.get("marker_found")) is not True
    elif name == "retained_order_loaded":
        o.present = True
        o.category = "LEGAL_HOLD_RECORD"
    else:
        return None
    return o


def parse_log(path, file_id, file_time):
    obs = []
    trace_keys: dict[str, set] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        ev = parse_log_line(line)
        if not ev:
            continue
        tid = ev.get("trace_id") or ""
        keys = [ev.get(k) for k in STARTED_KEYS if ev.get(k)]
        keys = [k for k in keys if not RESOURCE_RE.fullmatch(str(k))]
        if keys and tid:
            trace_keys.setdefault(tid, set()).update(idents_from(keys))
        o = log_event_obs(ev, trace_keys.get(tid, set()), file_id, file_time)
        if o:
            obs.append(o)
    return obs


# ---------------------------------------------------------------------------------------------- documents
def text_obs(text: str, file_id, file_time, source: str):
    """Business documents and screenshots: link every resource id mentioned to the identifiers around it."""
    obs = []
    rids = sorted(set(RESOURCE_RE.findall(text)))
    ids = idents_from(re.split(r"[\s|,;]+", text)) | idents_from([text])
    low = text.lower()
    for rid in rids:
        system = system_for(rid)
        o = Obs(file_id, file_time, file_time, rid, system, present=True, idents=frozenset(ids), source=source)
        if system == "support_platform" and ("attachment" in low or ".pdf" in low):
            o.category = "SUPPORT_ATTACHMENT"
            o.pii = bool(ids - {i for i in ids if i.startswith("user_")})
        obs.append(o)
    return obs, ids


def parse_pdf(path, file_id, file_time):
    from pypdf import PdfReader
    text = "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    obs, _ = text_obs(text, file_id, file_time, "pdf")
    return obs, text


# ---------------------------------------------------------------------------------------------- loader
def load_manifest():
    with open(DATASET / "evidence_files.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_all(ocr=None):
    """Parse every evidence file. Returns (observations, sql_coverage, raw_texts)."""
    observations, coverage, texts = [], [], {}
    for row in load_manifest():
        fid, ft = row["file_id"], row["captured_at"]
        path = DATASET / row["file_path"]
        ext = path.suffix.lower()
        if ext == ".sql":
            obs, cov = parse_sql(path, fid, ft)
            coverage.append(cov)
        elif ext == ".json":
            obs = parse_json(path, fid, ft, coverage)
        elif ext == ".log":
            obs = parse_log(path, fid, ft)
        elif ext == ".txt":
            obs = parse_txt(path, fid, ft)
        elif ext == ".pdf":
            obs, texts[fid] = parse_pdf(path, fid, ft)
        elif ext in (".png", ".jpg", ".jpeg") and ocr is not None:
            from .images import parse_image
            obs, texts[fid] = parse_image(path, fid, ft, ocr)
        else:
            obs = []
        observations.extend(obs)
    return observations, coverage, texts
