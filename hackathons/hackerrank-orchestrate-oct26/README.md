# Ghost Data Still Exists: Deletion-Audit Agent

An agent that proves whether a person's data was really deleted. For each request in
`dataset/deletion_requests.csv` it decides whether deletion was authorized, finds every copy of the person's
data across databases, replicas, logs, exports, support records, backups and screenshots, reconstructs the true
state at `audit_at`, applies `deletion_rules.csv`, and writes `COMPLETE`, `INCOMPLETE` or `NOT_APPLICABLE` with an
ordered, evidence-backed `steps_json`.

**Results on the 32 labelled samples:** status accuracy **100%**, step precision **100%**, step recall
**97.9%**, sequence accuracy **90.6%**. The three remaining gaps cannot be recovered from participant data (see
`code/evaluation/evaluation_report.md`). The full run audits 518 requests in seconds, at **$0.92** in Claude API
usage for the whole set.

---

## Quick start

Requires Python 3.10+.

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r code\requirements.txt
.venv\Scripts\python code\main.py                 # writes output.csv in the repository root
.venv\Scripts\python code\evaluation\main.py --report
```

**macOS / Linux**
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r code/requirements.txt
.venv/bin/python code/main.py
.venv/bin/python code/evaluation/main.py --report
```

### Optional: Claude API layer
Create a `.env` file in the repository root (it is git-ignored and never packaged):
```text
ANTHROPIC_API_KEY=<your key>
```
Without a key the agent runs the deterministic engine alone. Every decision is still made, and only the LLM
cross-checks and vision reading are skipped. On this dataset, that changes 5 of the 518 answers (`case_34`,
`case_39`, `case_45`, `case_50`, `case_53`): their deciding evidence is a screenshot whose state (a running
connector, an email still on screen) local OCR cannot judge on its own. The submitted `output.csv` was produced
with the key. Model responses are cached in `.cache/llm/`, so reruns are deterministic and cost nothing.

### Command reference
| Command | What it does |
|---|---|
| `python code/main.py` | Audit all 518 requests, write `output.csv`, run the contract checks, write `code/evaluation/usage_report.md` |
| `python code/main.py --requests dataset/sample_deletion_requests.csv --out sample_predictions.csv` | Audit any request file |
| `python code/main.py --no-llm` / `--no-ocr` | Switch off the Claude layer / screenshot OCR |
| `python code/evaluation/main.py [--diff]` | Score the 32 samples (and show mismatches) |
| `python code/evaluation/main.py --report` | Full study: ablations, custom cases, model comparisons → `evaluation_report.md` |
| `python code/tests/run_tests.py` | Unit tests for the core rules |

---

## How it works

```text
request ─► 1 intent ─► 2 identity ─► 3 discovery ─► 4 state at audit_at ─► 5 policy ─► 6 ordered steps
            rules +      current +     evidence +      latest citable        deletion_rules.csv   contract
            LLM check    historical    workflow        evidence wins;        (delete / redact /   order +
                         ids, hashes   reconstruction  claims never count    anonymize / retain)  validation
```

1. **Intent** (`intent.py`, `llm.py`): a multilingual rule classifier with explicit negation handling
   ("I am *not* asking for deletion"). Claude independently classifies every request in batches. They agreed
   on 550/550 texts, and the LLM settles only texts where no rule fires (e.g. a German request, `custom_06`).
2. **Identity** (`identity.py`): request email → stable `user_id` → every email, phone and SHA-256 email hash
   the person has had (`user_audit_log.csv`). Names are not used for linking because they are ambiguous.
3. **Discovery** (`evidence.py`, `images.py`, `workflow.py`): all 94 evidence files are parsed into one shape,
   *observations* ("resource R seen at time T, in state S, carrying identifiers I"):
   SQLite snapshots (executed in memory, primary vs replica tables), JSON bundles and read-back exports,
   9 log dialects (started/completed events joined by trace id), the text handover, PDFs (pypdf), and screenshots
   (local OCR plus Claude vision). Records are linked by exact identifiers. Records with no identifiers left (a
   404 account, a fully anonymized profile) are linked by **reconstructing the deletion workflow** from
   `system_activity.csv`. The account event's result mirrors the reported claim (validated on 252/252
   independently linked accounts), and each workflow's later steps share a seconds-phase fingerprint relative to
   that event. Accounts are assigned jointly across all requests, so one event serves one workflow.
4. **State at `audit_at`** (`pipeline.py`): only evidence captured at or before `audit_at` counts. The latest
   observation wins; explicit observations (a 404 read-back, a found record) beat absence-by-omission, which is
   used only to prove deletion of delete-category records. Workflow statuses and activity results are claims
   and never decide anything on their own.
5. **Policy** (`planner.py`): each resource's data category maps to its required action in
   `deletion_rules.csv`. Data flows that can re-create data and restorable backups are findings in their own
   right, and tombstones keep only the stable `user_id`.
6. **Steps**: findings → remediation (disable flows and block restores before changing records) →
   verification, ordered as the contract requires. COMPLETE cases contain only verifications that cite evidence
   proving the compliant state; INCOMPLETE cases add the account and retained-record checks that must pass after
   remediation. `main.py` validates every row against the contract before finishing.

### Complexity and cost
With *n* requests, *m* evidence observations and activity events, and *k* identifiers per person:
- Parsing is a single pass over every file: **O(m)**.
- Identifier, resource and per-user history look-ups use hash indexes: **O(1)** each.
- Activity-window queries (account candidates, workflow steps) use time-sorted indexes with binary search:
  **O(log m + window)** each.
- Overall: **O((n·k + m) log m)**. The full run takes about 4 s, of which about 3 s is loading the evidence.
- Claude is called 25 times for the whole set (intent batched 40 per call, plus 11 screenshots): **232
  tokens and $0.0018 per request**. Responses are cached, so reruns are free.

### Traps the agent handles
- **Claims vs truth**: `SUCCESS`, `PARTIAL` and `DELETION_PENDING` are not proof.
- **Decoys**: near-identical emails (`g.silva76.jr@` vs `g.silva76@`), and negative look-ups made months
  before the request that point at another person's account.
- **Historical identifiers**: in 80 evaluation cases, some data is reachable only through an old email,
  phone or hash.
- **Replication drift** (copies left in replicas) and **re-creation** (connectors repopulating deleted records).
- **Time**: evidence after `audit_at` is ignored. The cut-off is inclusive, and all timestamps are UTC.

---

## How AI was used

- **Inside the agent**: Claude (`claude-opus-5-5`, structured JSON output) gives an independent intent verdict
  for every request and reads every screenshot. A local neural OCR model (RapidOCR) also reads the screenshots.
  The deterministic engine makes the final decisions, so results are reproducible and explainable, and every
  disagreement between rules and models is measured in the evaluation report. Prompts are in `code/prompts/`.
- **Building the agent**: the solution was developed with Claude Code as a pair programmer: dataset
  reverse-engineering, hypothesis testing against the samples, implementation and evaluation. The full
  conversation is in `log.txt`.

---

## Repository layout (submitted `code.zip`)

```text
README.md
code/
  main.py                    CLI entry point, contract validation, usage report
  requirements.txt
  prompts/                   intent.md, screenshot.md (LLM prompts)
  ghost_audit/
    config.py                paths, step vocabulary and ordering, system/category maps
    evidence.py              evidence readers -> observations (SQL, JSON, logs, text, PDF)
    images.py                local OCR with on-disk cache
    llm.py                   optional Claude layer: batched intent, screenshot vision, caching, usage
    identity.py              current + historical identifiers
    intent.py                multilingual rule classifier with negation handling
    workflow.py              deletion-workflow reconstruction from system_activity.csv
    pipeline.py              global linking, state at audit_at, per-case audit
    planner.py               policy application and step ordering
  evaluation/
    main.py                  scoring, ablations, model comparisons, report generator
    custom_cases.py          7 custom (metamorphic) evaluation cases
    evaluation_report.md     generated metrics and analysis
    usage_report.md          generated token and cost report for the final run
  tests/run_tests.py         unit tests
```

The problem statement is in `problem_statement.md`, and the challenge instructions are in `AGENTS.md`.
