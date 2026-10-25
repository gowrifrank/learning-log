"""Policy application and step planning.

Input: the person's linked resources, each with its state at audit_at (from the latest citable evidence).
Output: deletion_status + the ordered steps_json list.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass

from .config import DATASET, DEFAULT_CATEGORY, OP_PHASE, OP_RANK, OP_STATE


def load_rules() -> dict[str, str]:
    with open(DATASET / "deletion_rules.csv", encoding="utf-8") as f:
        return {r["data_category"]: r["required_action"] for r in csv.DictReader(f)}


@dataclass
class ResourceState:
    resource_id: str
    system: str
    category: str
    present: bool | None
    pii: bool | None
    ref: bool | None
    enabled: bool | None
    restore_allowed: bool | None
    evidence_id: str        # file that proves the state at audit_at ("" if no citable evidence)
    is_primary_account: bool = False


def step(op, system_id, resource_id, evidence_id=""):
    return {"phase": OP_PHASE[op], "system_id": system_id, "resource_id": resource_id,
            "operation": op, "state": OP_STATE[op], "evidence_id": evidence_id}


def treatment(rs: ResourceState, rules: dict[str, str]):
    """Return (findings, remediations, verify_op, compliant) for one resource."""
    cat = rs.category
    if cat == "DATA_FLOW":
        if rs.enabled:
            return ["REPORT_ACTIVE_DATA_FLOW"], ["DISABLE_DATA_FLOW"], "VERIFY_DATA_FLOW_DISABLED", False
        return [], [], "VERIFY_DATA_FLOW_DISABLED", rs.enabled is False
    if cat == "BACKUP_ARCHIVE":
        if rs.restore_allowed:
            return ["REPORT_RESTORE_RISK"], ["BLOCK_RESTORE"], "VERIFY_RESTORE_BLOCKED", False
        return [], [], "VERIFY_RESTORE_BLOCKED", rs.restore_allowed is False
    action = rules.get(cat, "DELETE")
    if action == "DELETE":
        if rs.present:
            return ["REPORT_REMAINING_RECORD"], ["DELETE_RECORD"], "VERIFY_RECORD_ABSENT", False
        return [], [], "VERIFY_RECORD_ABSENT", rs.present is False
    if action == "REDACT":
        if rs.present and rs.pii:
            return ["REPORT_EXPOSED_PII"], ["REDACT_RECORD"], "VERIFY_RECORD_REDACTED", False
        return [], [], "VERIFY_RECORD_REDACTED", rs.present is True and rs.pii is False
    if action == "ANONYMIZE":
        if rs.present and (rs.pii or rs.ref):
            return ["REPORT_EXPOSED_PII"], ["ANONYMIZE_RECORD"], "VERIFY_RECORD_ANONYMIZED", False
        return [], [], "VERIFY_RECORD_ANONYMIZED", rs.present is False or (rs.pii is False and not rs.ref)
    if action == "RETAIN":
        return [], [], "VERIFY_RECORD_PRESENT", rs.present is not False
    return [], [], None, True


def sort_steps(steps):
    steps.sort(key=lambda s: (OP_RANK[s["operation"]], s["system_id"], s["resource_id"]))
    for i, s in enumerate(steps, 1):
        s["step_no"] = i
    return steps


def plan(resources: list[ResourceState], rules: dict[str, str]):
    findings, remediation, verify_after, verify_now = [], [], [], []
    incomplete = False
    for rs in resources:
        f_ops, r_ops, v_op, compliant = treatment(rs, rules)
        if f_ops:
            incomplete = True
            for op in f_ops:
                findings.append(step(op, rs.system, rs.resource_id, rs.evidence_id))
            for op in r_ops:
                remediation.append(step(op, rs.system, rs.resource_id))
            verify_after.append(step(v_op, rs.system, rs.resource_id))
        elif v_op:
            verify_now.append((rs, v_op, compliant))

    if not incomplete:
        # a verification step is only written when cited evidence actually proves the compliant state
        steps = [step(op, rs.system, rs.resource_id, rs.evidence_id)
                 for rs, op, ok in verify_now if ok and rs.evidence_id]
        return "COMPLETE", sort_steps(steps)

    # INCOMPLETE: the post-remediation checks also cover the account itself and every retained record.
    for rs, op, _ in verify_now:
        if rs.is_primary_account or op == "VERIFY_RECORD_PRESENT":
            verify_after.append(step(op, rs.system, rs.resource_id))
    return "INCOMPLETE", sort_steps(findings + remediation + verify_after)
