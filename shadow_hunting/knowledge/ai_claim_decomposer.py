"""Decompose a statement into observation / inference / conclusion layers.

Many AI errors collapse these three. The AI reads "childhood adversity blunts
threat response" and treats it as observation ("we measured X"), inference
("therefore Y"), and conclusion ("so do Z") simultaneously. Separating them
exposes what evidence the speaker actually has vs. what they concluded.

Used both ways: the AI decomposes the user's claims, and the AI decomposes
its own statements before emitting them.

License: CC0
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class ClaimLayer(Enum):
    OBSERVATION = "observation"
    INFERENCE = "inference"
    CONCLUSION = "conclusion"


OBSERVATION_CUES = (
    "observed", "measured", "recorded", "reported", "detected", "showed",
    "found that", "we saw", "data show", "signal", "was", "were",
)
INFERENCE_CUES = (
    "therefore", "thus", "hence", "implies", "suggests", "indicates",
    "means that", "associated with", "correlated", "explains", "because",
)
CONCLUSION_CUES = (
    "should", "must", "recommend", "policy", "we need", "requires",
    "is a", "is evidence of", "constitutes", "impairment", "deficit",
    "pathology", "disorder", "proves",
)


@dataclass
class DecomposedClaim:
    original: str
    observation: Optional[str] = None
    inference: Optional[str] = None
    conclusion: Optional[str] = None
    collapses: List[str] = field(default_factory=list)
    layer_cues_hit: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original,
            "observation": self.observation,
            "inference": self.inference,
            "conclusion": self.conclusion,
            "collapses": list(self.collapses),
            "layer_cues_hit": {k: list(v) for k, v in self.layer_cues_hit.items()},
        }

    def missing_layers(self) -> List[str]:
        out = []
        if not self.observation:
            out.append(ClaimLayer.OBSERVATION.value)
        if not self.inference:
            out.append(ClaimLayer.INFERENCE.value)
        if not self.conclusion:
            out.append(ClaimLayer.CONCLUSION.value)
        return out


def _find_cues(text: str, cues) -> List[str]:
    low = text.lower()
    return [c for c in cues if c in low]


def decompose(statement: str) -> DecomposedClaim:
    """Heuristic split. Not a parser — a prompt.

    Returns a DecomposedClaim with whatever layers the cue-matching could
    identify. Unidentified layers become questions the AI should ask the human
    (or itself) rather than quietly fill in.
    """
    obs_cues = _find_cues(statement, OBSERVATION_CUES)
    inf_cues = _find_cues(statement, INFERENCE_CUES)
    con_cues = _find_cues(statement, CONCLUSION_CUES)

    parts = re.split(r"[,;.]\s+|\s+—\s+|\s+-\s+", statement.strip())
    parts = [p for p in parts if p]

    observation: Optional[str] = None
    inference: Optional[str] = None
    conclusion: Optional[str] = None

    for p in parts:
        pl = p.lower()
        if any(c in pl for c in CONCLUSION_CUES) and conclusion is None:
            conclusion = p
        elif any(c in pl for c in INFERENCE_CUES) and inference is None:
            inference = p
        elif any(c in pl for c in OBSERVATION_CUES) and observation is None:
            observation = p

    if observation is None and inference is None and conclusion is None:
        if con_cues:
            conclusion = statement
        elif inf_cues:
            inference = statement
        else:
            observation = statement

    collapses: List[str] = []
    if con_cues and not obs_cues:
        collapses.append(
            "conclusion stated without an observable signal — the statement "
            "names an action or category but does not identify what was measured"
        )
    if con_cues and not inf_cues:
        collapses.append(
            "conclusion stated without the intermediate inference — jumps from "
            "observation (or nothing) directly to category/action"
        )
    if obs_cues and con_cues and not inf_cues:
        collapses.append(
            "observation and conclusion collapsed — the inference step connecting "
            "them is implicit"
        )

    return DecomposedClaim(
        original=statement,
        observation=observation,
        inference=inference,
        conclusion=conclusion,
        collapses=collapses,
        layer_cues_hit={
            ClaimLayer.OBSERVATION.value: obs_cues,
            ClaimLayer.INFERENCE.value: inf_cues,
            ClaimLayer.CONCLUSION.value: con_cues,
        },
    )


def decompose_as_prompt(statement: str) -> str:
    d = decompose(statement)
    lines = [
        "CLAIM DECOMPOSITION",
        "-" * 40,
        f"Original: {d.original}",
        "",
    ]
    if d.observation:
        lines.append(f"Observation layer: {d.observation}")
    else:
        lines.append("Observation layer: NOT IDENTIFIED — what was actually measured?")
    if d.inference:
        lines.append(f"Inference layer:   {d.inference}")
    else:
        lines.append("Inference layer:   NOT IDENTIFIED — what step connects observation to conclusion?")
    if d.conclusion:
        lines.append(f"Conclusion layer:  {d.conclusion}")
    else:
        lines.append("Conclusion layer:  NOT IDENTIFIED — what action or category is being asserted?")
    if d.collapses:
        lines.append("")
        lines.append("Collapses detected:")
        for c in d.collapses:
            lines.append(f"  ! {c}")
    return "\n".join(lines)
