"""Ghost Data Still Exists: deletion-audit agent.

Usage (from the repository root):
    python code/main.py                      # audit dataset/deletion_requests.csv -> output.csv
    python code/main.py --requests dataset/sample_deletion_requests.csv --out sample_predictions.csv
    python code/main.py --no-ocr             # skip screenshot OCR (faster, less evidence)
    python code/main.py --no-llm             # deterministic engine only (no Claude API calls)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ghost_audit.config import DATASET, REPO_ROOT  # noqa: E402
from ghost_audit.pipeline import Auditor  # noqa: E402


def make_ocr(enabled: bool):
    if not enabled:
        return None
    try:
        from ghost_audit.images import OcrEngine
        return OcrEngine()
    except ImportError as e:                       # OCR is optional; the rest of the evidence still works
        print(f"[warn] OCR unavailable ({e}); screenshots will be skipped", file=sys.stderr)
        return None


def make_llm(enabled: bool):
    if not enabled:
        return None
    from ghost_audit.llm import LlmLayer
    if not LlmLayer.available():
        print("[info] ANTHROPIC_API_KEY not set: running the deterministic engine only", file=sys.stderr)
        return None
    return LlmLayer()


def case_order(r) -> tuple:
    """Natural case order (case_33 < case_100), matching the input file and the expected answers."""
    head, _, num = r["case_id"].rpartition("_")
    return (head, int(num)) if num.isdigit() else (r["case_id"], 0)


def run(requests_path: Path, out_path: Path, ocr: bool = True, llm: bool = True,
        auditor: Auditor | None = None) -> list[dict]:
    auditor = auditor or Auditor(ocr=make_ocr(ocr), llm=make_llm(llm))
    with open(requests_path, encoding="utf-8") as f:
        requests = list(csv.DictReader(f))
    rows = []
    for req in sorted(requests, key=case_order):
        status, steps, _ = auditor.audit(req)
        rows.append({"case_id": req["case_id"], "deletion_status": status,
                     "steps_json": json.dumps(steps, separators=(",", ":"), ensure_ascii=False)})
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "deletion_status", "steps_json"])
        w.writeheader()
        w.writerows(rows)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--requests", default=str(DATASET / "deletion_requests.csv"))
    ap.add_argument("--out", default=str(REPO_ROOT / "output.csv"))
    ap.add_argument("--no-ocr", action="store_true")
    ap.add_argument("--no-llm", action="store_true", help="skip the Claude API layer even if a key is set")
    a = ap.parse_args()
    auditor = Auditor(ocr=make_ocr(not a.no_ocr), llm=make_llm(not a.no_llm))
    rows = run(Path(a.requests), Path(a.out), auditor=auditor)
    print(f"wrote {len(rows)} rows -> {a.out}")
    problems = validate(rows, Path(a.requests))
    print("contract checks:", "all passed" if not problems else f"{len(problems)} problems")
    for p in problems[:20]:
        print("   ", p)
    if auditor.llm is not None:
        print("llm usage:", auditor.llm.usage.totals())
        if Path(a.requests).resolve() == (DATASET / "deletion_requests.csv").resolve():
            from ghost_audit.config import CACHE_DIR
            report = Path(__file__).resolve().parent / "evaluation" / "usage_report.md"
            report.write_text(auditor.llm.usage.to_markdown(len(rows), CACHE_DIR / "llm"), encoding="utf-8")
            print(f"usage report -> {report}")
    sys.exit(1 if problems else 0)


PHASE_ORDER = {"FINDING": 0, "REMEDIATION": 1, "VERIFICATION": 2}


def validate(rows: list[dict], requests_path: Path) -> list[str]:
    """Check output.csv against the submission contract in problem_statement.md."""
    with open(DATASET / "evidence_files.csv", encoding="utf-8") as f:
        captured = {r["file_id"]: r["captured_at"] for r in csv.DictReader(f)}
    with open(requests_path, encoding="utf-8") as f:
        audit_at = {r["case_id"]: r["audit_at"] for r in csv.DictReader(f)}
    out = []
    ids = [r["case_id"] for r in rows]
    if ids != sorted(ids, key=lambda c: case_order({"case_id": c})) or set(ids) != set(audit_at)             or len(ids) != len(set(ids)):
        out.append("rows must be exactly one per request, sorted by case_id")
    for r in rows:
        cid, status, steps = r["case_id"], r["deletion_status"], json.loads(r["steps_json"])
        if status not in ("COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"):
            out.append(f"{cid}: bad status {status}")
        if status == "NOT_APPLICABLE" and steps:
            out.append(f"{cid}: NOT_APPLICABLE must have []")
        if [s["step_no"] for s in steps] != list(range(1, len(steps) + 1)):
            out.append(f"{cid}: step numbers not consecutive from 1")
        if [PHASE_ORDER[s["phase"]] for s in steps] != sorted(PHASE_ORDER[s["phase"]] for s in steps):
            out.append(f"{cid}: phases out of order")
        if status == "COMPLETE" and any(s["phase"] != "VERIFICATION" for s in steps):
            out.append(f"{cid}: COMPLETE may only contain verification steps")
        for s in steps:
            needs = s["phase"] == "FINDING" or status == "COMPLETE"
            e = s["evidence_id"]
            if needs and (e not in captured or captured[e] > audit_at[cid]):
                out.append(f"{cid}: step {s['step_no']} must cite evidence captured at or before audit_at")
            if not needs and e:
                out.append(f"{cid}: step {s['step_no']} is future work and must have an empty evidence_id")
    return out


if __name__ == "__main__":
    main()
