"""Provenance primitives for AI-facing outputs.

Every element emitted by the knowledge pipeline carries a provenance tag so an
AI consumer can distinguish what the user said, what a template always says,
what a heuristic actually matched, and what was composed from multiple signals.

Without these tags an AI tends to read templated output as insight. With them
the AI knows which items to investigate further with the human and which to
treat as scaffolding.

License: CC0
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class Provenance(Enum):
    USER_SUPPLIED = "user_supplied"
    TEMPLATE_UNIVERSAL = "template_universal"
    HEURISTIC_TRIGGERED = "heuristic_triggered"
    DERIVED = "derived"


@dataclass
class TaggedClaim:
    content: str
    provenance: Provenance
    trigger: Optional[str] = None
    source_fields: List[str] = field(default_factory=list)
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "provenance": self.provenance.value,
            "trigger": self.trigger,
            "source_fields": list(self.source_fields),
            "notes": self.notes,
        }


def user(content: str, source_field: str) -> TaggedClaim:
    return TaggedClaim(content, Provenance.USER_SUPPLIED, source_fields=[source_field])


def template(content: str, note: Optional[str] = None) -> TaggedClaim:
    return TaggedClaim(content, Provenance.TEMPLATE_UNIVERSAL, notes=note)


def heuristic(content: str, trigger: str, source_fields: Optional[List[str]] = None) -> TaggedClaim:
    return TaggedClaim(
        content,
        Provenance.HEURISTIC_TRIGGERED,
        trigger=trigger,
        source_fields=list(source_fields or []),
    )


def derived(content: str, source_fields: List[str], note: Optional[str] = None) -> TaggedClaim:
    return TaggedClaim(content, Provenance.DERIVED, source_fields=source_fields, notes=note)
