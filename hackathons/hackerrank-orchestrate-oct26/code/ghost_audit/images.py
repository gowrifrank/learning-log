"""Screenshot evidence: local OCR (RapidOCR / ONNX, no API key) + structured fact extraction.

OCR output is cached under .cache/ocr/ so repeated runs are fast and deterministic. The cache is derived
data (plain OCR text) and is rebuilt automatically when missing.
"""
from __future__ import annotations

import json
import re

from .config import CACHE_DIR, system_for
from .evidence import Obs, RESOURCE_RE, idents_from


class OcrEngine:
    def __init__(self):
        from rapidocr_onnxruntime import RapidOCR   # optional dependency
        self._ocr = None
        self._cls = RapidOCR
        (CACHE_DIR / "ocr").mkdir(parents=True, exist_ok=True)
        self.calls = 0

    def lines(self, path) -> list[dict]:
        cache = CACHE_DIR / "ocr" / (path.stem + ".json")
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))
        if self._ocr is None:
            self._ocr = self._cls()
        result, _ = self._ocr(str(path))
        self.calls += 1
        out = [{"text": t, "x": round(min(p[0] for p in box)), "y": round(min(p[1] for p in box)),
                "conf": round(float(c), 3)} for box, t, c in (result or [])]
        cache.write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
        return out


def _clean(t: str) -> str:
    """Undo the usual OCR slips on these screens (dropped spaces, stray glyphs)."""
    t = t.replace("�", " ").replace("·", " ")
    return re.sub(r"\s+", " ", t).strip()


STATE_WORDS = {
    "restore_allowed": [(r"\brestore (allowed|enabled)\b|\ballowed\b", True), (r"\bblocked\b|\bdenied\b|\bdisallowed\b", False)],
    "enabled": [(r"\benabled\b|\bactive\b|\brunning\b", True), (r"\bdisabled\b|\bstopped\b|\bpaused\b", False)],
}


def parse_image(path, file_id, file_time, ocr: OcrEngine):
    rows = ocr.lines(path)
    text = "\n".join(_clean(r["text"]) for r in rows)
    flat = " ".join(_clean(r["text"]) for r in rows)
    obs = []
    rids = sorted(set(RESOURCE_RE.findall(flat.replace(" ", "_") + " " + flat)))
    # group OCR lines into visual rows (same y within a few pixels) so a table row's resource id is tied to
    # the identifiers printed on that row rather than to everything on the screen
    by_row: dict[int, list] = {}
    for r in rows:
        by_row.setdefault(round(r["y"] / 12), []).append(_clean(r["text"]))
    row_text = {k: " ".join(v) for k, v in by_row.items()}
    for rid in rids:
        system = system_for(rid)
        mine = [t for t in row_text.values() if rid in t.replace(" ", "")]
        scope = " ".join(mine) if mine else flat
        ids = idents_from(re.split(r"[\s|,;:]+", scope))
        o = Obs(file_id, file_time, file_time, rid, system, present=True, idents=frozenset(ids), source="ocr")
        low = scope.lower()
        for attr, pats in STATE_WORDS.items():
            if (attr == "restore_allowed" and system == "backup_service") or (attr == "enabled" and system == "integration_service"):
                for pat, val in pats:
                    if re.search(pat, low):
                        setattr(o, attr, val)
                        break
        obs.append(o)
    return obs, text
