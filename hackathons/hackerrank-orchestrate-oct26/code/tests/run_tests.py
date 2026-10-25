"""Unit tests for the core rules. Run: python code/tests/run_tests.py (no test framework needed)."""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ghost_audit import evidence as ev  # noqa: E402
from ghost_audit.identity import IdentityIndex  # noqa: E402
from ghost_audit.intent import classify  # noqa: E402
from ghost_audit.planner import ResourceState, load_rules, plan  # noqa: E402
from ghost_audit.workflow import same_workflow, ts  # noqa: E402

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


# ------------------------------------------------------------------------------------------------ intent
@test
def deletion_requests_in_six_languages():
    for text in ["Please erase the account linked to this email address.",
                 "Solicito la eliminación permanente de la cuenta asociada a este correo.",
                 "Solicito a exclusão permanente da conta associada a este e-mail.",
                 "Je demande la suppression définitive du compte associé à cette adresse e-mail.",
                 "이 이메일 주소에 연결된 계정의 영구 삭제를 요청합니다.",
                 "このメールアドレスに関連するアカウントの完全な削除を依頼します。",
                 "Please check that my profile is gone and remove anything left."]:
        assert classify(text)[0], text


@test
def negation_and_lookalikes_are_not_deletion():
    for text in ["I still need the account and my order history, so I am not asking for deletion.",
                 "I still use it, so please don't delete or change anything.",
                 "Please remove me from marketing lists only.",
                 "I'd like to download my account information in a portable format.",
                 "My surname is misspelled on the account. Can you correct it without removing any of my records?",
                 "This is an information request, not a request to erase it."]:
        assert not classify(text)[0], text


# ------------------------------------------------------------------------------------------------ identity
@test
def historical_and_upper_case_emails_resolve_to_the_same_person():
    idx = IdentityIndex()
    a = idx.resolve("abena.o189491@zoho.com")
    b = idx.resolve("ABENA.O1894@ZOHO.COM")
    assert a.user_id and a.user_id == b.user_id
    assert {"abena.o189466@zoho.com", "abena.o189491@zoho.com", "abena.o1894@zoho.com"} <= a.emails
    assert len(a.hashes) >= 3                                   # a hash for every historical email


# ------------------------------------------------------------------------------------------------ logs
@test
def every_log_dialect_parses_to_the_same_fields():
    lines = [
        '2026-09-15T11:51:20Z level=INFO service=account_service trace_id=t1 resource_id=account_4745 '
        'event=profile_lookup_completed rows=0 http_status=404',
        '2026-02-22T10:58:51Z [DEBUG] [account_service] [t1] profile_lookup_completed: resource_id="account_4745" '
        'rows="0" http_status="404"',
        '2026-07-03T07:51:32Z | DEBUG | account_service | t1 | profile_lookup_completed | resource_id="account_4745" '
        'rows="0" http_status="404"',
        '2026-04-19T06:51:13Z {"service":"account_service","trace_id":"t1","event":"profile_lookup_completed",'
        '"resource_id":"account_4745","rows":"0","http_status":"404"}',
        '2026-08-22T10:51:17Z <15>1 node-1 account_service t1 - - resource_id="account_4745" '
        'event="profile_lookup_completed" rows="0" http_status="404"',
        '2026-06-08T06:52:09Z requestId=t1 level=INFO function=account_service message="resource_id=\\"account_4745\\" '
        'event=\\"profile_lookup_completed\\" rows=\\"0\\" http_status=\\"404\\""',
    ]
    for line in lines:
        e = ev.parse_log_line(line)
        o = ev.log_event_obs(e, set(), "f", "t")
        assert o and o.resource_id == "account_4745" and o.present is False, line


# ------------------------------------------------------------------------------------------------ workflow
@test
def workflow_fingerprint_matches_phase_not_minutes():
    t0 = ts("2026-08-30T10:57:28Z")
    assert same_workflow(t0, ts("2026-08-30T11:31:09Z"))       # +33m41s: first pre-report treatment
    assert same_workflow(t0, ts("2026-08-30T11:38:38Z"))       # +41m10s
    assert not same_workflow(t0, ts("2026-08-30T11:31:53Z"))   # +34m25s: another workflow's step
    assert not same_workflow(t0, ts("2026-08-30T10:50:00Z"))   # before the account event


# ------------------------------------------------------------------------------------------------ planner
def rs(rid, system, cat, evidence="evidence_01", primary=False, **state):
    base = dict(present=None, pii=None, ref=None, enabled=None, restore_allowed=None)
    base.update(state)
    return ResourceState(rid, system, cat, evidence_id=evidence, is_primary_account=primary, **base)


@test
def incomplete_plan_is_ordered_and_future_steps_have_no_evidence():
    rules = load_rules()
    status, steps = plan([
        rs("account_1", "account_service", "USER_PROFILE", primary=True, present=False),
        rs("search_9", "search_service", "SEARCH_INDEX_ENTRY", present=True),
        rs("support_2", "support_platform", "SUPPORT_MESSAGE", present=True, pii=True),
        rs("data_flow_3", "integration_service", "DATA_FLOW", enabled=True),
        rs("audit_record_4", "security_service", "SECURITY_AUDIT_LOG", present=True),
    ], rules)
    assert status == "INCOMPLETE"
    ops = [s["operation"] for s in steps]
    assert ops == ["REPORT_REMAINING_RECORD", "REPORT_EXPOSED_PII", "REPORT_ACTIVE_DATA_FLOW",
                   "DISABLE_DATA_FLOW", "DELETE_RECORD", "REDACT_RECORD",
                   "VERIFY_RECORD_ABSENT", "VERIFY_RECORD_ABSENT", "VERIFY_RECORD_PRESENT",
                   "VERIFY_RECORD_REDACTED", "VERIFY_DATA_FLOW_DISABLED"], ops
    assert [s["step_no"] for s in steps] == list(range(1, len(steps) + 1))
    assert all(s["evidence_id"] for s in steps if s["phase"] == "FINDING")
    assert not any(s["evidence_id"] for s in steps if s["phase"] != "FINDING")


@test
def complete_plan_only_verifies_what_evidence_proves():
    rules = load_rules()
    status, steps = plan([
        rs("account_1", "account_service", "USER_PROFILE", primary=True, present=False),
        rs("analytics_5", "analytics_platform", "ANALYTICS_PROFILE", present=True, pii=False, ref=False),
        rs("analytics_6", "analytics_platform", "ANALYTICS_PROFILE", present=True),   # state unknown
    ], rules)
    assert status == "COMPLETE"
    assert [(s["operation"], s["resource_id"]) for s in steps] == [
        ("VERIFY_RECORD_ABSENT", "account_1"), ("VERIFY_RECORD_ANONYMIZED", "analytics_5")]


@test
def tombstone_keeps_reference_but_not_identifiers():
    rules = load_rules()
    status, steps = plan([rs("tombstone_1", "identity_service", "ACCOUNT_TOMBSTONE", present=True, pii=True,
                             ref=True)], rules)
    assert status == "INCOMPLETE" and steps[1]["operation"] == "REDACT_RECORD"
    status, steps = plan([rs("tombstone_1", "identity_service", "ACCOUNT_TOMBSTONE", present=True, pii=False,
                             ref=True)], rules)
    assert status == "COMPLETE" and steps[0]["operation"] == "VERIFY_RECORD_REDACTED"


def main():
    failed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL  {fn.__name__}")
            traceback.print_exc()
    print(f"\n{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
