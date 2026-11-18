"""Small deterministic context selection primitives (Week 8).

The token estimate is a documented character heuristic, not a tokenizer.
"""
from dataclasses import dataclass
import math
import re
from datetime import datetime, timezone


@dataclass(frozen=True)
class ContextItem:
    identifier: str
    text: str
    role: str
    provenance: str
    trust: str
    revision: str
    created_at: float
    ttl_seconds: float | None = None

    def __post_init__(self):
        if not all(isinstance(x, str) and x for x in (self.identifier,self.text,self.role,self.provenance,self.revision)):
            raise ValueError("nonempty context fields required")
        if self.trust not in {"untrusted", "observed", "verified", "policy"}:
            raise ValueError("unknown trust class")
        if self.role not in {"system", "developer", "user", "assistant", "tool"}:
            raise ValueError("unknown message role")
        if self.role in {"system", "developer"} and self.trust != "policy":
            raise ValueError("system/developer role requires policy-authored context")
        if self.trust == "policy" and self.role not in {"system", "developer"}:
            raise ValueError("policy trust requires system/developer role")
        if type(self.created_at) not in {int,float} or not math.isfinite(self.created_at): raise ValueError("finite created_at required")
        if self.ttl_seconds is not None and (type(self.ttl_seconds) not in {int,float} or not math.isfinite(self.ttl_seconds) or self.ttl_seconds < 0):
            raise ValueError("ttl must be finite and nonnegative")

    def fresh(self, now: float) -> bool:
        return self.ttl_seconds is None or now <= self.created_at + self.ttl_seconds


def estimate_tokens(text: str) -> int:
    """Conservative-ish educational estimate; never exact model token accounting."""
    if not isinstance(text,str): raise ValueError("text required")
    return (len(text.encode("utf-8")) + 3) // 4


def select_context(items, query, *, token_budget, now, reserved=()):
    """Select fresh items by lexical overlap, then authority and stable ID.

    Reserved items retain caller order and are charged before ranked evidence.
    Returned context is deterministic for the same inputs.
    """
    if type(token_budget) is not int or token_budget < 0 or type(now) not in {int,float} or not math.isfinite(now):
        raise ValueError("invalid budget or clock")
    items=list(items); reserved=list(reserved)
    if not isinstance(query,str) or any(not isinstance(x,ContextItem) for x in items+reserved):
        raise ValueError("query and context items required")
    if len({x.identifier for x in items+reserved}) != len(items)+len(reserved): raise ValueError("duplicate context id")
    if any(not x.fresh(now) for x in reserved): raise ValueError("reserved context is stale")
    used=sum(estimate_tokens(x.text) for x in reserved)
    if used > token_budget: raise ValueError("reserved context exceeds budget")
    terms=lambda s:set(re.findall(r"[a-z0-9]+",s.casefold()))
    q=terms(query); rank={"policy":3,"verified":2,"observed":1,"untrusted":0}
    candidates=[x for x in items if x.fresh(now) and x.identifier not in {r.identifier for r in reserved}]
    candidates.sort(key=lambda x:(-len(q & terms(x.text)), -rank[x.trust], -x.created_at, x.identifier))
    selected=list(reserved)
    for item in candidates:
        cost=estimate_tokens(item.text)
        if used+cost<=token_budget: selected.append(item);used+=cost
    return selected


@dataclass(frozen=True)
class CompactedContext:
    text: str
    source_refs: tuple[str,...]
    source_revisions: tuple[str,...]
    lossy: bool=True
    authority: str="summary is untrusted derived text; original authority is not inherited"


def compact(items, *, max_chars=500):
    """Create a deliberately lossy excerpt retaining references and revisions."""
    marker="[TRUNCATED]"
    if type(max_chars) is not int or max_chars < len(marker): raise ValueError("max_chars must fit the truncation marker")
    items=list(items)
    if any(not isinstance(x,ContextItem) for x in items): raise ValueError("ContextItem records required")
    refs=tuple(x.identifier for x in items); revisions=tuple(x.revision for x in items)
    joined="\n".join(x.text for x in items)
    text=joined[:max_chars]
    if len(joined)>max_chars:
        prefix=max_chars-len(marker)
        text=(joined[:prefix-1]+"\n" if prefix>1 else "")+marker
    return CompactedContext(text,refs,revisions)


def utc_timestamp(value: datetime) -> float:
    if value.tzinfo is None: raise ValueError("timezone-aware timestamp required")
    return value.astimezone(timezone.utc).timestamp()
