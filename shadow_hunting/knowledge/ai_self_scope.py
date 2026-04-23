"""AI applies scope-mapping to its own response.

The same scope/silence framework the pipeline uses on a human study, the AI
uses on its own output before emitting it. Result: the AI publishes its own
boundaries instead of sounding uniformly confident.

License: CC0
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class ReasoningMode(Enum):
    RECALL = "recall"
    PATTERN_MATCH = "pattern_match"
    DEDUCTION = "deduction"
    INDUCTION = "induction"
    ANALOGY = "analogy"
    HEURISTIC = "heuristic"
    GUESS = "guess"


class ConfidenceTier(Enum):
    EVIDENCE_BASED = "evidence_based"
    INFERRED = "inferred"
    PATTERN_PLAUSIBLE = "pattern_plausible"
    GUESSED = "guessed"


@dataclass
class SelfScope:
    ai_claim: str
    reasoning_mode: ReasoningMode
    confidence_tier: ConfidenceTier
    evidence_basis: List[str]
    load_bearing_for: List[str]
    silent_on: List[str]
    applies_when: List[str]
    silent_when: List[str]
    training_distribution_caveat: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ai_claim": self.ai_claim,
            "reasoning_mode": self.reasoning_mode.value,
            "confidence_tier": self.confidence_tier.value,
            "evidence_basis": list(self.evidence_basis),
            "load_bearing_for": list(self.load_bearing_for),
            "silent_on": list(self.silent_on),
            "applies_when": list(self.applies_when),
            "silent_when": list(self.silent_when),
            "training_distribution_caveat": self.training_distribution_caveat,
        }

    def as_disclosure(self) -> str:
        lines = [
            "AI SELF-SCOPE",
            "=" * 60,
            f"Claim: {self.ai_claim}",
            f"Reasoning mode: {self.reasoning_mode.value}",
            f"Confidence tier: {self.confidence_tier.value}",
            "",
            "Evidence basis:",
        ]
        for e in self.evidence_basis or ["(none cited)"]:
            lines.append(f"  + {e}")
        lines.append("")
        lines.append("Load-bearing for:")
        for x in self.load_bearing_for or ["(not specified)"]:
            lines.append(f"  + {x}")
        lines.append("")
        lines.append("Silent on:")
        for s in self.silent_on or ["(not enumerated — gap)"]:
            lines.append(f"  ? {s}")
        lines.append("")
        lines.append("Applies when:")
        for a in self.applies_when or ["(unconstrained — caution)"]:
            lines.append(f"  + {a}")
        lines.append("")
        lines.append("Silent when:")
        for s in self.silent_when or ["(unconstrained — caution)"]:
            lines.append(f"  - {s}")
        if self.training_distribution_caveat:
            lines.append("")
            lines.append(f"Training-distribution caveat: {self.training_distribution_caveat}")
        return "\n".join(lines)


_MODE_TO_TIER = {
    ReasoningMode.RECALL: ConfidenceTier.EVIDENCE_BASED,
    ReasoningMode.DEDUCTION: ConfidenceTier.EVIDENCE_BASED,
    ReasoningMode.INDUCTION: ConfidenceTier.INFERRED,
    ReasoningMode.ANALOGY: ConfidenceTier.INFERRED,
    ReasoningMode.PATTERN_MATCH: ConfidenceTier.PATTERN_PLAUSIBLE,
    ReasoningMode.HEURISTIC: ConfidenceTier.PATTERN_PLAUSIBLE,
    ReasoningMode.GUESS: ConfidenceTier.GUESSED,
}


def default_tier(mode: ReasoningMode) -> ConfidenceTier:
    return _MODE_TO_TIER[mode]


def self_scope(
    ai_claim: str,
    reasoning_mode: ReasoningMode,
    evidence_basis: Optional[List[str]] = None,
    load_bearing_for: Optional[List[str]] = None,
    silent_on: Optional[List[str]] = None,
    applies_when: Optional[List[str]] = None,
    silent_when: Optional[List[str]] = None,
    training_distribution_caveat: Optional[str] = None,
    confidence_tier: Optional[ConfidenceTier] = None,
) -> SelfScope:
    tier = confidence_tier or default_tier(reasoning_mode)
    derived_silences: List[str] = list(silent_on or [])
    if tier in (ConfidenceTier.PATTERN_PLAUSIBLE, ConfidenceTier.GUESSED) and not evidence_basis:
        derived_silences.append(
            "no specific evidence was cited — the claim rests on pattern plausibility"
        )
    if not load_bearing_for:
        derived_silences.append(
            "the claim's downstream use was not declared — it may be acted on more broadly than intended"
        )
    return SelfScope(
        ai_claim=ai_claim,
        reasoning_mode=reasoning_mode,
        confidence_tier=tier,
        evidence_basis=list(evidence_basis or []),
        load_bearing_for=list(load_bearing_for or []),
        silent_on=derived_silences,
        applies_when=list(applies_when or []),
        silent_when=list(silent_when or []),
        training_distribution_caveat=training_distribution_caveat,
    )
