"""Identity resolution: request email -> stable user_id -> every identifier the person has ever used."""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass, field

from .config import DATASET
from .evidence import norm_phone


@dataclass
class Identity:
    user_id: str | None
    emails: set = field(default_factory=set)
    hashes: set = field(default_factory=set)
    phones: set = field(default_factory=set)
    names: set = field(default_factory=set)
    audit_ids: list = field(default_factory=list)     # user_audit_log rows that proved a historical identifier

    @property
    def keys(self) -> set:
        """Identifiers used for exact linking against evidence (names are too ambiguous to link on)."""
        ks = set(self.emails) | set(self.hashes) | {"tel:" + p for p in self.phones}
        if self.user_id:
            ks.add(self.user_id)
        return ks


def sha(email: str) -> str:
    return hashlib.sha256(email.lower().encode()).hexdigest()


class IdentityIndex:
    def __init__(self):
        with open(DATASET / "user_identities.csv", encoding="utf-8") as f:
            self.users = {r["user_id"]: r for r in csv.DictReader(f)}
        with open(DATASET / "user_audit_log.csv", encoding="utf-8") as f:
            self.audit = list(csv.DictReader(f))
        self.by_email: dict[str, set] = {}
        self.audit_by_user: dict[str, list] = {}          # O(1) access to one person's history
        for uid, u in self.users.items():
            self.by_email.setdefault(u["email"].lower(), set()).add(uid)
        for a in self.audit:
            self.audit_by_user.setdefault(a["user_id"], []).append(a)
            if a["field_name"] == "email":
                for v in (a["old_value"], a["new_value"]):
                    if v:
                        self.by_email.setdefault(v.lower(), set()).add(a["user_id"])

    def resolve(self, email: str, as_of: str | None = None) -> Identity:
        uids = self.by_email.get(email.lower(), set())
        if len(uids) != 1:
            # unknown address (or ambiguous): we can still search evidence for the address itself
            return Identity(None, emails={email.lower()}, hashes={sha(email)})
        uid = next(iter(uids))
        u = self.users[uid]
        ident = Identity(uid)
        ident.emails.add(u["email"].lower())
        ident.emails.add(email.lower())
        ident.hashes.add(u["email_hash"].lower())
        ident.phones.add(norm_phone(u["phone"]))
        ident.names.add(u["name"].lower())
        for a in self.audit_by_user.get(uid, ()):
            if as_of and a["event_time"] > as_of:
                continue
            ident.audit_ids.append(a["audit_id"])
            for v in (a["old_value"], a["new_value"]):
                if not v:
                    continue
                if a["field_name"] == "email":
                    ident.emails.add(v.lower())
                elif a["field_name"] == "email_hash":
                    ident.hashes.add(v.lower())
                elif a["field_name"] == "phone":
                    ident.phones.add(norm_phone(v))
                elif a["field_name"] == "name":
                    ident.names.add(v.lower())
        ident.hashes |= {sha(e) for e in ident.emails}
        ident.phones.discard("")
        return ident
