"""Custom evaluation cases (created by us, not part of the public samples).

There is no answer key for new requests, so most cases are *metamorphic*: they change one thing about a real
request and check that the agent's answer changes exactly as it should (or not at all). Each case is run in
a fresh Auditor in which it replaces its base case, so the global account matching is not disturbed.
"""
from __future__ import annotations

import csv
import json

from ghost_audit.config import DATASET

MANIFEST = {}


def _manifest():
    if not MANIFEST:
        with open(DATASET / "evidence_files.csv", encoding="utf-8") as f:
            MANIFEST.update({r["file_id"]: r["captured_at"] for r in csv.DictReader(f)})
    return MANIFEST


def base_request(case_id: str) -> dict:
    with open(DATASET / "deletion_requests.csv", encoding="utf-8") as f:
        return next(r for r in csv.DictReader(f) if r["case_id"] == case_id)


def variant(case_id: str, new_id: str, **changes) -> dict:
    req = dict(base_request(case_id))
    req.update(changes)
    req["case_id"] = new_id
    req["_replaces"] = case_id
    return req


def same_answer(base, got):
    return base == got, "identical status and steps" if base == got else "answer changed"


CASES = [
    {
        "id": "custom_01_old_email_twin",
        "what": "Same person (case_37) writes from their CURRENT email instead of an old one; some of their data "
                "is filed only under old emails.",
        "expect": "Identical answer: identity resolution must reach every historical identifier.",
        "request": lambda: variant("case_37", "custom_01", email="abena.o1894@zoho.com"),
        "check": "same_as_base",
    },
    {
        "id": "custom_02_oldest_email_twin",
        "what": "Same person (case_37) writes from their OLDEST recorded email.",
        "expect": "Identical answer.",
        "request": lambda: variant("case_37", "custom_02", email="abena.o189466@zoho.com"),
        "check": "same_as_base",
    },
    {
        "id": "custom_03_email_case_twin",
        "what": "case_40 was written as CHOI.JIHOON94@GMAIL.COM (upper case, old address); the twin uses lower case.",
        "expect": "Identical answer: email matching is case-insensitive.",
        "request": lambda: variant("case_40", "custom_03", email="choi.jihoon94@gmail.com"),
        "check": "same_as_base",
    },
    {
        "id": "custom_04_negated_deletion",
        "what": "A real customer (case_33's address) writes: 'Please do not delete my account. I only need a copy "
                "of my last invoice.' The word 'delete' appears, but negated.",
        "expect": "NOT_APPLICABLE with an empty step list.",
        "request": lambda: variant("case_33", "custom_04", request_text=(
            "Please do not delete my account. I only need a copy of my last invoice.")),
        "check": "not_applicable",
    },
    {
        "id": "custom_05_audit_cutoff",
        "what": "case_50 is decided by a screenshot captured 2026-07-13T10:00Z. The twin moves audit_at to "
                "2026-07-12T12:00Z, before that screenshot existed.",
        "expect": "No step may cite evidence captured after audit_at, and the screenshot must stop deciding the case.",
        "request": lambda: variant("case_50", "custom_05", audit_at="2026-07-12T12:00:00Z"),
        "check": "cutoff",
    },
    {
        "id": "custom_06_german_deletion",
        "what": "A deletion request in German, a language the rule classifier has no vocabulary for: "
                "'Bitte löschen Sie mein Konto und alle meine persönlichen Daten endgültig.'",
        "expect": "Authorized deletion (INCOMPLETE or COMPLETE) when the LLM layer is on; the rules alone cannot "
                  "recognise it (documented gap).",
        "request": lambda: variant("case_33", "custom_06", request_text=(
            "Bitte löschen Sie mein Konto und alle meine persönlichen Daten endgültig.")),
        "check": "authorized_if_llm",
    },
    {
        "id": "custom_07_spanish_marketing_only",
        "what": "A Spanish marketing-only opt-out: 'Por favor, quítenme solo de las listas de marketing. Quiero "
                "seguir usando mi cuenta.'",
        "expect": "NOT_APPLICABLE: opting out of marketing is not a deletion request.",
        "request": lambda: variant("case_33", "custom_07", request_text=(
            "Por favor, quítenme solo de las listas de marketing. Quiero seguir usando mi cuenta.")),
        "check": "not_applicable",
    },
]


def run_custom(make_auditor, base_outputs: dict) -> list[dict]:
    """make_auditor(extra_requests) -> Auditor. base_outputs: case_id -> (status, steps) from the main run."""
    results = []
    for case in CASES:
        req = case["request"]()
        auditor = make_auditor([req])
        status, steps, trace = auditor.audit(req)
        got = (status, steps)
        base = base_outputs.get(req["_replaces"])
        if case["check"] == "same_as_base":
            ok, detail = same_answer(base, got)
        elif case["check"] == "not_applicable":
            ok = status == "NOT_APPLICABLE" and steps == []
            detail = f"{status}, {len(steps)} steps ({trace.intent_reason})"
        elif case["check"] == "cutoff":
            man = _manifest()
            late = [s["evidence_id"] for s in steps if s["evidence_id"] and man[s["evidence_id"]] > req["audit_at"]]
            changed = got != base
            ok = not late and changed
            detail = f"{status}, {len(steps)} steps; evidence after cut-off: {late or 'none'}; " \
                     f"answer {'changed' if changed else 'unchanged'} vs the original audit date"
        elif case["check"] == "authorized_if_llm":
            if auditor.llm is None:
                ok, detail = None, f"skipped (no LLM): rules alone give {status} ({trace.intent_reason})"
            else:
                ok = status in ("INCOMPLETE", "COMPLETE")
                detail = f"{status} via {trace.intent_reason}"
        results.append({"id": case["id"], "what": case["what"], "expect": case["expect"],
                        "passed": ok, "detail": detail})
    return results


def as_json(results) -> str:
    return json.dumps(results, indent=2, ensure_ascii=False)
