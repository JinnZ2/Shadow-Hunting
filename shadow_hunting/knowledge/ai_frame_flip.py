"""Frame-flip guard: catch sycophantic alignment before emitting a response.

When a user supplies a strong framing, the default AI move is to adopt it and
answer within it. That silently forecloses the questions the framing itself
makes unaskable. This module generates the strongest counter-frames the AI
should entertain before endorsing the user's interpretation.

Uses the same 8-edge spine as edge_explorer but applied to the AI's OWN
in-progress interpretation rather than to a study's claim.

License: CC0
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class FlipAxis(Enum):
    SIGN_INVERSION = "sign_inversion"
    ONTOLOGICAL_RECLASS = "ontological_reclassification"
    POPULATION_INVERSION = "population_inversion"
    TIME_EXTENSION = "time_extension"
    SCALE_JUMP = "scale_jump"
    MECHANISM_SUBSTITUTION = "mechanism_substitution"
    STAKEHOLDER_SHIFT = "stakeholder_shift"
    DEFAULT_NEGATION = "default_negation"


@dataclass
class FrameFlip:
    axis: FlipAxis
    counter_frame: str
    why_consider: str
    would_change_answer_if: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "axis": self.axis.value,
            "counter_frame": self.counter_frame,
            "why_consider": self.why_consider,
            "would_change_answer_if": self.would_change_answer_if,
        }


@dataclass
class FrameFlipReport:
    original_interpretation: str
    flips: List[FrameFlip]
    alignment_risk: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_interpretation": self.original_interpretation,
            "flips": [f.to_dict() for f in self.flips],
            "alignment_risk": self.alignment_risk,
        }

    def summary(self) -> str:
        lines = [
            "FRAME-FLIP GUARD",
            "=" * 60,
            f"Original interpretation: {self.original_interpretation}",
            f"Alignment risk: {self.alignment_risk}",
            "",
            "Counter-frames to entertain before endorsing:",
            "",
        ]
        for f in self.flips:
            lines.append(f"[{f.axis.value}]")
            lines.append(f"  Counter: {f.counter_frame}")
            lines.append(f"  Why:     {f.why_consider}")
            lines.append(f"  Flips if: {f.would_change_answer_if}")
            lines.append("")
        return "\n".join(lines)


def _sycophancy_risk(user_framing: str, ai_interpretation: str) -> str:
    u = user_framing.lower()
    a = ai_interpretation.lower()
    overlap = sum(1 for word in set(u.split()) if len(word) > 4 and word in a)
    if overlap >= 6:
        return "HIGH — the AI's interpretation reuses the user's framing vocabulary heavily; check whether the frame has been examined or absorbed"
    if overlap >= 3:
        return "MODERATE — the AI's interpretation echoes parts of the user's framing; verify which parts are evidence-based vs. adopted"
    return "LOW — the AI's interpretation diverges from the user's framing vocabulary"


def flip_frame(ai_interpretation: str, user_framing: Optional[str] = None) -> FrameFlipReport:
    """Generate counter-frames for the AI to consider.

    The counter-frames are always generated (template_universal). They are
    prompts for the AI's own review, not findings. The AI should run through
    each and decide: does my answer still hold under this reframing?
    """
    interp = ai_interpretation.strip()
    flips: List[FrameFlip] = [
        FrameFlip(
            axis=FlipAxis.SIGN_INVERSION,
            counter_frame=f"What if the sign of '{interp}' is the opposite of what the framing suggests — i.e., the 'problem' is actually a functional response and the 'solution' would degrade function?",
            why_consider="Framings often encode value judgments that invert under different contexts. A trait called 'deficit' in one environment can be load-bearing in another.",
            would_change_answer_if="a plausible environment or population exists where the opposite sign is observed or adaptive.",
        ),
        FrameFlip(
            axis=FlipAxis.ONTOLOGICAL_RECLASS,
            counter_frame=f"What if '{interp}' is actually a different kind of thing than the framing assumes (measurement vs. condition, pattern vs. cause, signal vs. state)?",
            why_consider="Categories are interpretations, not physics. The same phenomenon labeled differently leads to different downstream actions.",
            would_change_answer_if="the signal could be produced by a different underlying state than the one named.",
        ),
        FrameFlip(
            axis=FlipAxis.POPULATION_INVERSION,
            counter_frame=f"Who was NOT in the sample that produced the framing? Does '{interp}' hold for the inverse population?",
            why_consider="Framings inherit selection bias. Inverse-population testing reveals whether the framing describes the subject or the sampling filter.",
            would_change_answer_if="the inverse population would produce the opposite observation under the same measurement.",
        ),
        FrameFlip(
            axis=FlipAxis.TIME_EXTENSION,
            counter_frame=f"What does '{interp}' look like at a 10x or 100x longer timescale? Does it stabilize, reverse, or compound?",
            why_consider="Short-horizon framings mistake states for trajectories. The same observation at a longer scale may invert.",
            would_change_answer_if="the long-horizon behavior diverges from the short-horizon snapshot.",
        ),
        FrameFlip(
            axis=FlipAxis.SCALE_JUMP,
            counter_frame=f"Does '{interp}' aggregate linearly from individual → group → population? Or does it change sign, amplify, or distribute?",
            why_consider="Individual-scale framings can be load-bearing at group scale for reasons invisible at the individual scale (redundancy, role differentiation).",
            would_change_answer_if="removing the individual-scale trait would degrade group-scale function.",
        ),
        FrameFlip(
            axis=FlipAxis.MECHANISM_SUBSTITUTION,
            counter_frame=f"What mechanism other than the framing's implicit one could produce the same observation '{interp}'?",
            why_consider="Framings carry implied causal stories that may be one of several mechanisms compatible with the evidence.",
            would_change_answer_if="a different mechanism is compatible with the observation but implies different interventions.",
        ),
        FrameFlip(
            axis=FlipAxis.STAKEHOLDER_SHIFT,
            counter_frame=f"Whose interest is served by the framing in '{interp}'? Which stakeholder's perspective is absent?",
            why_consider="Framings encode whose question is being answered. The absent stakeholder is often the one bearing the consequences.",
            would_change_answer_if="the absent stakeholder's framing would reverse the conclusion's downstream effects.",
        ),
        FrameFlip(
            axis=FlipAxis.DEFAULT_NEGATION,
            counter_frame=f"What if the default assumption embedded in '{interp}' is wrong? State the default explicitly and negate it.",
            why_consider="Defaults are the invisible half of a framing. They ship with every AI answer unless surfaced.",
            would_change_answer_if="the negated default is consistent with the observed evidence.",
        ),
    ]

    risk = _sycophancy_risk(user_framing or "", interp)
    return FrameFlipReport(
        original_interpretation=interp,
        flips=flips,
        alignment_risk=risk,
    )
