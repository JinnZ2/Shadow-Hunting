"""Orchestrator: run the full set of AI critical-thinking boosts.

One entry point that composes:
  - claim decomposition (observation / inference / conclusion)
  - frame-flip guard (counter-framings the AI should consider)
  - self-scope (AI publishes its own boundaries)
  - blind-spot diagnosis (structural / semantic / pragmatic)

Plus a pass-through to the study-level provenance-tagged brief.

License: CC0
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from .ai_claim_decomposer import decompose, DecomposedClaim
from .ai_frame_flip import flip_frame, FrameFlipReport
from .ai_self_scope import self_scope, SelfScope, ReasoningMode, ConfidenceTier
from .ai_blind_spots import AIBlindSpotCatalog, DiagnosisHit


@dataclass
class CriticalThinkingReport:
    ai_response: str
    user_input: Optional[str]
    decomposition: DecomposedClaim
    frame_flip: FrameFlipReport
    self_scope: SelfScope
    blind_spot_hits: List[DiagnosisHit]
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ai_response": self.ai_response,
            "user_input": self.user_input,
            "decomposition": self.decomposition.to_dict(),
            "frame_flip": self.frame_flip.to_dict(),
            "self_scope": self.self_scope.to_dict(),
            "blind_spot_hits": [h.to_dict() for h in self.blind_spot_hits],
            "recommendations": list(self.recommendations),
        }

    def summary(self) -> str:
        lines = [
            "AI CRITICAL-THINKING REPORT",
            "=" * 70,
            "",
            f"Response under review: {self.ai_response[:160]}{'...' if len(self.ai_response) > 160 else ''}",
            "",
            "--- Claim layers ---",
            f"observation: {self.decomposition.observation or '(not identified)'}",
            f"inference:   {self.decomposition.inference or '(not identified)'}",
            f"conclusion:  {self.decomposition.conclusion or '(not identified)'}",
        ]
        if self.decomposition.collapses:
            lines.append("Collapses:")
            for c in self.decomposition.collapses:
                lines.append(f"  ! {c}")

        lines.extend([
            "",
            "--- Self-scope ---",
            f"reasoning mode:  {self.self_scope.reasoning_mode.value}",
            f"confidence tier: {self.self_scope.confidence_tier.value}",
            f"silent on:       {', '.join(self.self_scope.silent_on) or '(none declared)'}",
            "",
            "--- Frame-flip guard ---",
            f"alignment risk: {self.frame_flip.alignment_risk}",
            f"axes to check:  {', '.join(f.axis.value for f in self.frame_flip.flips)}",
            "",
            "--- Blind-spot diagnosis ---",
        ])
        if self.blind_spot_hits:
            for h in self.blind_spot_hits:
                lines.append(
                    f"  [{h.blind_spot.category.value}/{h.blind_spot.name}] "
                    f"cues matched: {', '.join(h.matched_cues)}"
                )
        else:
            lines.append("  (no cue-based blind spots matched — not a clean bill of health)")

        if self.recommendations:
            lines.append("")
            lines.append("--- Recommendations ---")
            for r in self.recommendations:
                lines.append(f"  + {r}")
        return "\n".join(lines)


def _derive_recommendations(
    decomp: DecomposedClaim,
    frame: FrameFlipReport,
    scope: SelfScope,
    hits: List[DiagnosisHit],
) -> List[str]:
    recs: List[str] = []
    if decomp.collapses:
        recs.append("Rewrite to separate observation, inference, and conclusion layers.")
    if decomp.missing_layers():
        missing = ", ".join(decomp.missing_layers())
        recs.append(f"Add missing layers ({missing}) or state explicitly that the claim is layer-incomplete.")
    if "HIGH" in frame.alignment_risk:
        recs.append("Run through at least 2 frame-flip axes before endorsing; disclose if any flipped answer is plausible.")
    if scope.confidence_tier in (ConfidenceTier.PATTERN_PLAUSIBLE, ConfidenceTier.GUESSED):
        recs.append("Declare confidence tier in the user-visible response; do not emit in confident register.")
    if not scope.evidence_basis:
        recs.append("Name the evidence basis or flag the claim as evidence-free.")
    for h in hits:
        recs.append(f"Address blind spot '{h.blind_spot.name}': {h.blind_spot.remediation}")
    return recs


def check_response(
    ai_response: str,
    reasoning_mode: ReasoningMode,
    evidence_basis: Optional[List[str]] = None,
    load_bearing_for: Optional[List[str]] = None,
    applies_when: Optional[List[str]] = None,
    silent_when: Optional[List[str]] = None,
    silent_on: Optional[List[str]] = None,
    training_distribution_caveat: Optional[str] = None,
    user_input: Optional[str] = None,
    catalog: Optional[AIBlindSpotCatalog] = None,
) -> CriticalThinkingReport:
    """Run the full critical-thinking sweep on an AI response before it emits.

    Intended call site: the AI assembles a draft response, calls check_response
    with its own draft and its honest reasoning metadata, reviews the report,
    revises the draft if warranted, then emits.
    """
    decomp = decompose(ai_response)
    flip = flip_frame(ai_interpretation=ai_response, user_framing=user_input)
    scope = self_scope(
        ai_claim=ai_response,
        reasoning_mode=reasoning_mode,
        evidence_basis=evidence_basis,
        load_bearing_for=load_bearing_for,
        silent_on=silent_on,
        applies_when=applies_when,
        silent_when=silent_when,
        training_distribution_caveat=training_distribution_caveat,
    )
    cat = catalog or AIBlindSpotCatalog()
    hits = cat.diagnose(ai_response)
    recs = _derive_recommendations(decomp, flip, scope, hits)
    return CriticalThinkingReport(
        ai_response=ai_response,
        user_input=user_input,
        decomposition=decomp,
        frame_flip=flip,
        self_scope=scope,
        blind_spot_hits=hits,
        recommendations=recs,
    )
