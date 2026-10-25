# Usage Report: Ghost Data Still Exists

_Written automatically by `python code/main.py` after the full run that produced `output.csv`._

## Final full-dataset run

- Requests audited: **518** (`dataset/deletion_requests.csv`)
- Provider / model: **Anthropic / `claude-opus-5-5`** (effort `low`, structured JSON output), priced at $4.00 / $20.00 per million input / output tokens
- Local model: **RapidOCR** (PP-OCR detection + recognition, ONNX) for the 11 screenshots: runs on the CPU, 0 tokens, $0
- The deterministic engine (evidence parsing, identity, workflow reconstruction, policy, ordering) makes no model calls.

| Task | Model calls | Input tokens | Output tokens | Total tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| Intent classification (batched, 40 requests per call) | 14 | 51,724 | 25,470 | 77,194 | $0.7163 |
| Screenshot reading (vision) | 11 | 41,056 | 1,897 | 42,953 | $0.2022 |
| **Overall** | **25** | **92,780** | **27,367** | **120,147** | **$0.9185** |

- Average per request: **232 tokens**, **$0.00177**
- Intent batches also cover the 32 sample requests (550 texts in 14 calls), so the batches are identical for the evaluation and production runs and are served from one cache.
- Of these calls, 25 were served from the local response cache on this run; the token counts above are the original calls' recorded usage, so the cost shown is what producing this output cost, not the cost of the rerun (a rerun costs $0).

## Evaluation-only calls (not part of the production run)

- 7 calls made by `code/evaluation/main.py --report` for the custom evaluation cases: 6,062 input + 449 output tokens, $0.0332.
- One connectivity check during development: 18 input + 4 output tokens (about $0.0002).

## Token efficiency choices

- The LLM is used only where interpretation is needed (free-text intent, screenshots); all 518 decisions and step plans are deterministic.
- Requests are batched 40 per call instead of 518 single calls.
- Responses are cached by a hash of model + prompt + input, so reruns and evaluations are free and repeatable.
- `effort: low` with a strict JSON schema keeps output short and machine-checkable.
