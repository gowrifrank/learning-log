"""Workflow reconstruction from system_activity.csv.

Some records carry no identifiers at all once they are processed: a deleted account answers 404 and an
anonymized analytics profile has every identifier nulled. The only thing that ties them to a person is the
deletion workflow that touched them. This module rebuilds those workflows.

Observed structure of the deletion workflow (validated on every account that evidence links independently):
  * the deletion worker submits the primary profile 44-76 minutes before the workflow reports its status
    (hand-built legacy cases: within ~10 minutes of the report);
  * the account event's reported_result mirrors the workflow claim
    (COMPLETE -> SUCCESS, PARTIALLY_COMPLETE -> PARTIAL, NOT_STARTED -> FAILED);
  * every later step of the same workflow runs at a fixed seconds-phase relative to that account event:
    treatments before the report at +..41s/+..10s/+..40s/+..09s, follow-up operations after the report at
    +..52s/+..22s/+..51s/+..21s. That phase is a fingerprint that separates workflows reported at the same time.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import datetime, timedelta

CLAIM_TO_RESULT = {"COMPLETE": "SUCCESS", "PARTIALLY_COMPLETE": "PARTIAL", "NOT_STARTED": "FAILED"}
PRE_PHASES = (41, 10, 40, 9)
POST_PHASES = (52, 22, 51, 21)


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _phase_error(r: float, phases) -> float:
    return min(min(abs(r - p), 60 - abs(r - p)) for p in phases)


def phase_error(t_account: datetime, t_event: datetime) -> float | None:
    """Seconds away from the workflow fingerprint (None = outside the workflow's time span)."""
    d = (t_event - t_account).total_seconds()
    if d <= 0:
        return None
    minutes, r = d / 60, d % 60
    if 12 <= minutes <= 80:
        return _phase_error(r, PRE_PHASES)
    if 80 < minutes <= 240:
        return _phase_error(r, POST_PHASES)
    return None


def same_workflow(t_account: datetime, t_event: datetime) -> bool:
    err = phase_error(t_account, t_event)
    return err is not None and err <= 1.0


class TimeIndex:
    """Events sorted by time; a window query is two binary searches, O(log n + k)."""

    def __init__(self, events: list[dict]):
        self.events = sorted(events, key=lambda a: (a["event_time"], a["activity_id"]))
        self.times = [ts(a["event_time"]) for a in self.events]

    def window(self, lo: datetime, hi: datetime) -> list[dict]:
        return self.events[bisect_left(self.times, lo):bisect_right(self.times, hi)]


class WorkflowIndex:
    def __init__(self, activity: list[dict]):
        self.worker = [a for a in activity if a["source_system"] == "deletion_worker"]
        self.account_events = [a for a in self.worker if a["target_system"] == "account_service"
                               and a["event_type"] == "DELETE_RECORD"]
        self.events_by_res = defaultdict(list)
        for a in self.worker:
            self.events_by_res[a["resource_id"]].append(a)
        self._accounts = TimeIndex(self.account_events)
        self._worker = TimeIndex(self.worker)

    def account_candidates(self, req) -> list[dict]:
        rep = ts(req["reported_at"])
        want = CLAIM_TO_RESULT.get(req["reported_status"])
        out = [a for a in self._accounts.window(rep - timedelta(minutes=80), rep - timedelta(minutes=40))
               if want is None or a["reported_result"] == want]
        # legacy hand-run workflows: account event within ~10 minutes of the report, result not mirrored
        legacy = self._accounts.window(rep - timedelta(minutes=12), rep + timedelta(minutes=12))
        return out or legacy

    def chain_events(self, account_event: dict) -> list[dict]:
        t0 = ts(account_event["event_time"])
        span = self._worker.window(t0 + timedelta(minutes=12), t0 + timedelta(minutes=240))
        return [a for a in span if a is not account_event and same_workflow(t0, ts(a["event_time"]))]

    def account_event_for(self, account_id: str, req) -> dict | None:
        rep = ts(req["reported_at"])
        evs = [a for a in self.events_by_res.get(account_id, ()) if a["event_type"] == "DELETE_RECORD"
               and abs(rep - ts(a["event_time"])) <= timedelta(hours=3)]
        return min(evs, key=lambda a: abs(rep - ts(a["event_time"]))) if evs else None
