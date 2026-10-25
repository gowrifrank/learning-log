"""Optional LLM / vision layer (Claude API).

The deterministic engine makes every decision on its own. When ANTHROPIC_API_KEY is available this module
adds two independent model opinions:

  1. intent classification of every request text (batched), compared against the rule classifier;
  2. vision extraction of every screenshot into structured facts, cross-checked against local OCR.

Every response is cached on disk (keyed by model + prompt + input), so reruns are deterministic and free, and
every call's token usage is recorded for code/evaluation/usage_report.md.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path

from .config import CACHE_DIR, CODE_DIR, REPO_ROOT

MODEL = "claude-opus-5-5"
PRICES = {"claude-opus-5-5": (4.00, 20.00)}          # USD per million input / output tokens
PROMPTS = CODE_DIR / "prompts"
BATCH = 40

INTENT_SCHEMA = {
    "type": "object",
    "properties": {"results": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "case_id": {"type": "string"},
            "authorizes_deletion": {"type": "boolean"},
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "reason": {"type": "string"},
        },
        "required": ["case_id", "authorizes_deletion", "confidence", "reason"],
        "additionalProperties": False}}},
    "required": ["results"],
    "additionalProperties": False,
}

SCREEN_SCHEMA = {
    "type": "object",
    "properties": {
        "screen": {"type": "string"},
        "captured_at": {"type": "string"},
        "records": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "resource_id": {"type": "string"},
                "emails": {"type": "array", "items": {"type": "string"}},
                "user_refs": {"type": "array", "items": {"type": "string"}},
                "phones": {"type": "array", "items": {"type": "string"}},
                "state": {"type": "string", "enum": ["present", "absent", "redacted", "anonymized",
                                                     "flow_enabled", "flow_disabled", "restore_allowed",
                                                     "restore_blocked", "unknown"]},
                "shows_personal_data": {"type": "boolean"},
            },
            "required": ["resource_id", "emails", "user_refs", "phones", "state", "shows_personal_data"],
            "additionalProperties": False}},
    },
    "required": ["screen", "captured_at", "records"],
    "additionalProperties": False,
}


def load_dotenv(path: Path = REPO_ROOT / ".env") -> None:
    """Minimal .env reader (KEY=VALUE lines). Never overrides variables already set in the environment."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            if v.strip():
                os.environ.setdefault(k.strip(), v.strip())


class Usage:
    def __init__(self):
        self.by_task = defaultdict(lambda: defaultdict(int))
        self.files: set[str] = set()          # cache entries used by this run (one per model call)

    def add(self, task: str, usage: dict, cached: bool, cache_file: str = ""):
        t = self.by_task[task]
        t["calls"] += 1
        t["cache_hits"] += int(cached)
        t["input_tokens"] += usage.get("input_tokens", 0)
        t["output_tokens"] += usage.get("output_tokens", 0)
        if cache_file:
            self.files.add(cache_file)

    def to_markdown(self, n_requests: int, cache_dir: Path) -> str:
        pin, pout = PRICES[MODEL]
        tot = self.totals()
        L = ["# Usage Report: Ghost Data Still Exists", "",
             "_Written automatically by `python code/main.py` after the full run that produced `output.csv`._", "",
             "## Final full-dataset run", "",
             f"- Requests audited: **{n_requests}** (`dataset/deletion_requests.csv`)",
             f"- Provider / model: **Anthropic / `{MODEL}`** (effort `low`, structured JSON output), "
             f"priced at ${pin:.2f} / ${pout:.2f} per million input / output tokens",
             "- Local model: **RapidOCR** (PP-OCR detection + recognition, ONNX) for the 11 screenshots: "
             "runs on the CPU, 0 tokens, $0",
             "- The deterministic engine (evidence parsing, identity, workflow reconstruction, policy, ordering) "
             "makes no model calls.", "",
             "| Task | Model calls | Input tokens | Output tokens | Total tokens | Est. cost (USD) |",
             "|---|---|---|---|---|---|"]
        for task, t in sorted(self.by_task.items()):
            cost = t["input_tokens"] / 1e6 * pin + t["output_tokens"] / 1e6 * pout
            label = {"intent": "Intent classification (batched, 40 requests per call)",
                     "screenshot": "Screenshot reading (vision)"}.get(task, task)
            L.append(f"| {label} | {t['calls']} | {t['input_tokens']:,} | {t['output_tokens']:,} | "
                     f"{t['input_tokens'] + t['output_tokens']:,} | ${cost:.4f} |")
        total_tokens = tot["input_tokens"] + tot["output_tokens"]
        L += [f"| **Overall** | **{tot['calls']}** | **{tot['input_tokens']:,}** | **{tot['output_tokens']:,}** | "
              f"**{total_tokens:,}** | **${tot['cost_usd']:.4f}** |", "",
              f"- Average per request: **{total_tokens / n_requests:,.0f} tokens**, "
              f"**${tot['cost_usd'] / n_requests:.5f}**",
              "- Intent batches also cover the 32 sample requests (550 texts in 14 calls), so the batches are "
              "identical for the evaluation and production runs and are served from one cache.",
              f"- Of these calls, {tot['cache_hits']} were served from the local response cache on this run; the "
              "token counts above are the original calls' recorded usage, so the cost shown is what producing "
              "this output cost, not the cost of the rerun (a rerun costs $0).", ""]
        extra = [p for p in sorted(cache_dir.glob("*.json")) if p.name not in self.files]
        if extra:
            ein = eout = 0
            for p in extra:
                u = json.loads(p.read_text(encoding="utf-8"))["usage"]
                ein, eout = ein + u["input_tokens"], eout + u["output_tokens"]
            L += ["## Evaluation-only calls (not part of the production run)", "",
                  f"- {len(extra)} calls made by `code/evaluation/main.py --report` for the custom evaluation "
                  f"cases: {ein:,} input + {eout:,} output tokens, ${ein / 1e6 * pin + eout / 1e6 * pout:.4f}.",
                  "- One connectivity check during development: 18 input + 4 output tokens (about $0.0002).", ""]
        L += ["## Token efficiency choices", "",
              "- The LLM is used only where interpretation is needed (free-text intent, screenshots); "
              "all 518 decisions and step plans are deterministic.",
              "- Requests are batched 40 per call instead of 518 single calls.",
              "- Responses are cached by a hash of model + prompt + input, so reruns and evaluations are free and "
              "repeatable.",
              "- `effort: low` with a strict JSON schema keeps output short and machine-checkable.", ""]
        return "\n".join(L)

    def totals(self) -> dict:
        tot = defaultdict(int)
        for t in self.by_task.values():
            for k, v in t.items():
                tot[k] += v
        pin, pout = PRICES[MODEL]
        tot["cost_usd"] = tot["input_tokens"] / 1e6 * pin + tot["output_tokens"] / 1e6 * pout
        return dict(tot)


class LlmLayer:
    def __init__(self, model: str = MODEL):
        load_dotenv()
        import anthropic                      # optional dependency, only needed when a key is configured
        self.client = anthropic.Anthropic()
        self.model = model
        self.usage = Usage()
        self.dir = CACHE_DIR / "llm"
        self.dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def available() -> bool:
        load_dotenv()
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return False
        try:
            import anthropic  # noqa: F401
        except ImportError:
            return False
        return True

    # ---------------------------------------------------------------------------------------- core call
    def _call(self, task: str, system: str, content, schema: dict, cache_key: str) -> dict:
        path = self.dir / f"{task}-{cache_key[:24]}.json"
        if path.exists():
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.usage.add(task, saved["usage"], cached=True, cache_file=path.name)
            return saved["data"]
        resp = self.client.beta.messages.create(
            model=self.model,
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": content}],
            output_config={"effort": "low", "format": {"type": "json_schema", "schema": schema}},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",                       # a declined request is retried on a fallback model
        )
        if resp.stop_reason == "refusal":
            raise RuntimeError(f"{task}: model declined the request")
        text = next(b.text for b in resp.content if b.type == "text")
        data = json.loads(text)
        usage = {"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
                 "model": resp.model}
        path.write_text(json.dumps({"data": data, "usage": usage}, ensure_ascii=False, indent=1),
                        encoding="utf-8")
        self.usage.add(task, usage, cached=False, cache_file=path.name)
        return data

    # ---------------------------------------------------------------------------------------- tasks
    def classify_intents(self, requests: list[dict]) -> dict[str, dict]:
        system = (PROMPTS / "intent.md").read_text(encoding="utf-8")
        out = {}
        reqs = sorted(requests, key=lambda r: r["case_id"])
        for i in range(0, len(reqs), BATCH):
            chunk = [{"case_id": r["case_id"], "message": r["request_text"]} for r in reqs[i:i + BATCH]]
            body = json.dumps(chunk, ensure_ascii=False, indent=0)
            key = hashlib.sha256((self.model + system + body).encode()).hexdigest()
            data = self._call("intent", system, body, INTENT_SCHEMA, key)
            for res in data["results"]:
                out[res["case_id"]] = res
        return out

    def read_screenshot(self, path: Path) -> dict:
        system = (PROMPTS / "screenshot.md").read_text(encoding="utf-8")
        raw = path.read_bytes()
        key = hashlib.sha256(self.model.encode() + system.encode() + raw).hexdigest()
        content = [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                         "data": base64.standard_b64encode(raw).decode()}},
            {"type": "text", "text": "Extract the records shown in this screenshot."},
        ]
        return self._call("screenshot", system, content, SCREEN_SCHEMA, key)
