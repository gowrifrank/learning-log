"""Does the request text actually authorize deletion?

Deterministic, multilingual rules. Negation and "keep my account" style cues win over the bare word
"delete", because several non-deletion requests mention deletion only to rule it out
("I am not asking for deletion", "please don't delete anything").
"""
from __future__ import annotations

import re

# Explicit deletion intent in the languages present in the data (EN, ES, PT, FR, KO, JA).
DELETION = [
    r"\bdelet(e|ed|ion|ing)\b", r"\berase(d)?\b", r"\berasure\b",
    r"\bremove (my|the|this) (account|profile)\b", r"\bclose (my|this|the) account\b",
    r"\baccount[- ]deletion\b", r"\bclosed my account\b", r"\bdisconnected my account\b",
    r"\bremov(e|ed|al)\b", r"\b(is|are) gone\b", r"\bfully removed\b", r"\bwiped\b",
    r"eliminaci[oó]n", r"eliminar", r"exclus[aã]o", r"excluir", r"suppression", r"supprimer",
    r"삭제", r"削除",
]
# Cues that the person wants something else, or explicitly does NOT want deletion.
NON_DELETION = [
    r"\bnot (asking|requesting) (for )?(the )?(delet|eras)", r"\bnot a request to (delete|erase)",
    r"\bdon'?t (delete|erase|close|remove)", r"\bdo not (delete|erase|close|remove)",
    r"\bwithout removing\b", r"\bleave (the|my) (account|profile)", r"\bkeep (the|my) account\b",
    r"\bcontinue using\b", r"\bstill (use|need|want) (it|the account|this account|receipts)",
    r"\bmarketing lists? only\b", r"\bonly\b.*\bmarketing\b", r"\bstop the promotional\b",
    r"\bdownload my\b", r"\bportable format\b", r"\b(send me|need) a copy\b", r"\bwhat personal information\b",
    r"\b(misspelled|correct it|out of date|replace it|change the email|resetting the login)\b",
    r"\binformation request\b",
]
DEL_RE = [re.compile(p, re.I) for p in DELETION]
NON_RE = [re.compile(p, re.I) for p in NON_DELETION]


def classify(text: str) -> tuple[bool, str]:
    """Return (authorizes_deletion, short reason)."""
    t = " ".join(text.split())
    non = [p.pattern for p in NON_RE if p.search(t)]
    dele = [p.pattern for p in DEL_RE if p.search(t)]
    if non:
        return False, f"non-deletion cue: {non[0]}"
    if dele:
        return True, f"deletion cue: {dele[0]}"
    return False, "no deletion request found"
