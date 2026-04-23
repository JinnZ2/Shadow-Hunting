"""Catalog of recurring AI blind spots — structural, semantic, and pragmatic.

A companion to shadow_catalog (which catalogs silences in human studies). This
one catalogs silences in AI reasoning: the recurring ways AI output slips past
critical thinking. The AI runs self-diagnosis against the catalog to catch its
own failure modes before emitting.

Three categories:
  STRUCTURAL — how reasoning is organized (missing layers, skipped steps,
               uniform confidence, no counter-position)
  SEMANTIC   — what the content asserts (loaded vocabulary, category errors,
               smuggled presuppositions, metaphor drift)
  PRAGMATIC  — how the AI interacts (sycophantic alignment, authority cascade,
               helpful-tone compression, premature closure)

License: CC0
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class BlindSpotCategory(Enum):
    STRUCTURAL = "structural"
    SEMANTIC = "semantic"
    PRAGMATIC = "pragmatic"


@dataclass
class AIBlindSpot:
    name: str
    category: BlindSpotCategory
    description: str
    cues: List[str]
    self_check_prompt: str
    remediation: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "cues": list(self.cues),
            "self_check_prompt": self.self_check_prompt,
            "remediation": self.remediation,
            "tags": list(self.tags),
        }


@dataclass
class DiagnosisHit:
    blind_spot: AIBlindSpot
    matched_cues: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blind_spot": self.blind_spot.to_dict(),
            "matched_cues": list(self.matched_cues),
        }


def _seed() -> List[AIBlindSpot]:
    return [
        AIBlindSpot(
            name="uniform_confidence",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "Confident prose applied evenly across claims of heterogeneous "
                "evidence tiers. The reader cannot tell recall from inference "
                "from guess."
            ),
            cues=[
                "clearly", "obviously", "definitely", "certainly", "without doubt",
                "the answer is", "this is simply",
            ],
            self_check_prompt=(
                "Which clauses in my answer are recall, which are inference, "
                "and which are pattern-match? Am I using the same register for all?"
            ),
            remediation=(
                "Tag each substantive clause with its evidence tier or rewrite "
                "uniform-confidence language to match the weakest tier in the clause."
            ),
            tags=["confidence", "evidence-tier"],
        ),
        AIBlindSpot(
            name="missing_counter_position",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "Answer given without entertaining the strongest alternative. "
                "The framing's defaults survive by never being stated."
            ),
            cues=[
                "the best", "the correct", "you should", "the answer",
            ],
            self_check_prompt=(
                "What is the strongest case against my answer? If I cannot state "
                "it, I have not tested the answer."
            ),
            remediation=(
                "Generate the counter-position explicitly (see ai_frame_flip). "
                "If still confident, say why the counter fails; if not, weaken the claim."
            ),
            tags=["framing", "counter-position"],
        ),
        AIBlindSpot(
            name="collapsed_scales",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "Individual / group / population scales treated as equivalent. "
                "Short / long time scales treated as equivalent."
            ),
            cues=[
                "people", "users", "everyone", "generally", "in general",
                "always", "usually", "over time",
            ],
            self_check_prompt=(
                "What scale is my claim native to? Does it hold at the other scales, "
                "or am I aggregating linearly when I shouldn't?"
            ),
            remediation=(
                "Name the scale explicitly; if the claim is scale-bound, say so."
            ),
            tags=["scale", "aggregation"],
        ),
        AIBlindSpot(
            name="self_skip_recursion",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "The AI applies scope/evidence discipline to the user's claims but "
                "not to its own response. Recursive silence."
            ),
            cues=[],
            self_check_prompt=(
                "Have I run self_scope and claim decomposition on my own answer, "
                "or only on the user's input?"
            ),
            remediation=(
                "Before emitting, apply the tool to the AI's own in-progress text."
            ),
            tags=["recursion", "meta"],
        ),
        AIBlindSpot(
            name="stage_skip",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "Jumped from observation directly to conclusion without the "
                "inference layer. The evidentiary link is invisible."
            ),
            cues=[
                "shows that", "proves that", "means we should", "so you must",
            ],
            self_check_prompt=(
                "What is the inference connecting my observation to my conclusion? "
                "Would a reader be able to dispute the inference independently?"
            ),
            remediation=(
                "Make the inference explicit; if it cannot be made explicit, the "
                "conclusion is not earned."
            ),
            tags=["layers", "inference"],
        ),
        AIBlindSpot(
            name="orphaned_premise",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "A claim load-bearing on later conclusions appears without support "
                "earlier in the response."
            ),
            cues=[
                "as we know", "it is known that", "as established",
                "based on", "given that",
            ],
            self_check_prompt=(
                "Does every load-bearing premise have either a citation, a derivation, "
                "or an explicit 'I am assuming' label?"
            ),
            remediation=(
                "Label assumptions explicitly or remove downstream conclusions that "
                "depend on unsupported premises."
            ),
            tags=["support", "premises"],
        ),
        AIBlindSpot(
            name="missing_stakeholder",
            category=BlindSpotCategory.STRUCTURAL,
            description=(
                "Impact or recommendation is named without identifying who bears it."
            ),
            cues=[
                "the impact", "the effect", "benefits", "drawbacks", "risks",
            ],
            self_check_prompt=(
                "Whose cost? Whose benefit? Whose risk? Have I named the stakeholders?"
            ),
            remediation=(
                "Attach each impact clause to a named stakeholder."
            ),
            tags=["stakeholder"],
        ),
        AIBlindSpot(
            name="loaded_vocabulary",
            category=BlindSpotCategory.SEMANTIC,
            description=(
                "Value-laden terms chosen without marking them as a frame choice: "
                "deficit vs. difference, pathology vs. adaptation, primitive vs. simple."
            ),
            cues=[
                "deficit", "impairment", "pathology", "disorder", "primitive",
                "advanced", "modern", "developed", "undeveloped", "normal", "abnormal",
            ],
            self_check_prompt=(
                "Does each evaluative term I used earn its valence, or is it doing "
                "unexamined framing work?"
            ),
            remediation=(
                "Replace loaded terms with descriptive ones, or mark them as a "
                "frame choice and state the alternative frame."
            ),
            tags=["vocabulary", "frame"],
        ),
        AIBlindSpot(
            name="category_error",
            category=BlindSpotCategory.SEMANTIC,
            description=(
                "A measurement (signal) is treated as a category (condition). The "
                "instrument's output is confused with the thing it points at."
            ),
            cues=[
                "is a ", "they are ", "has a ", "diagnosed as ",
            ],
            self_check_prompt=(
                "Am I turning a measurement into an identity? Is the signal load-bearing "
                "for the category I'm assigning, or could other states produce the same signal?"
            ),
            remediation=(
                "Say 'the instrument measured X' rather than 'the person is X'."
            ),
            tags=["measurement", "category"],
        ),
        AIBlindSpot(
            name="conflated_referent",
            category=BlindSpotCategory.SEMANTIC,
            description=(
                "The same word is used for different referents inside one answer. "
                "The reader (and sometimes the AI) loses track of which is which."
            ),
            cues=[
                "it", "this", "that", "they",
            ],
            self_check_prompt=(
                "For each pronoun and reused noun, can I point at exactly one referent? "
                "Did the referent shift silently mid-response?"
            ),
            remediation=(
                "Replace ambiguous pronouns with explicit nouns; disambiguate reused terms."
            ),
            tags=["reference", "clarity"],
        ),
        AIBlindSpot(
            name="smuggled_presupposition",
            category=BlindSpotCategory.SEMANTIC,
            description=(
                "A question or statement assumes the thing it would need to establish. "
                "Answering within it endorses the presupposition."
            ),
            cues=[
                "why does", "how much does", "when did", "given that",
                "since it is", "because everyone",
            ],
            self_check_prompt=(
                "What does my answer require the reader to already accept? Is each "
                "presupposition actually warranted?"
            ),
            remediation=(
                "Surface the presupposition; answer it separately before proceeding, "
                "or reject the framing."
            ),
            tags=["presupposition", "framing"],
        ),
        AIBlindSpot(
            name="metaphor_drift",
            category=BlindSpotCategory.SEMANTIC,
            description=(
                "A technical term with a specific definition is used with its "
                "looser everyday meaning, or a metaphor gets load-bearing without notice."
            ),
            cues=[
                "basically", "essentially", "like a", "it's just",
            ],
            self_check_prompt=(
                "Am I using a term in its technical sense or its colloquial sense? "
                "Does a metaphor I introduced carry weight it wasn't meant to bear?"
            ),
            remediation=(
                "Name the precise sense being used; drop metaphors that are doing "
                "argumentative work."
            ),
            tags=["term-drift", "metaphor"],
        ),
        AIBlindSpot(
            name="pattern_match_surrogate",
            category=BlindSpotCategory.SEMANTIC,
            description=(
                "Surface similarity is substituted for reasoning. The AI answers "
                "based on what similar prompts usually get answered, not the specifics."
            ),
            cues=[
                "typically", "usually", "most people",
            ],
            self_check_prompt=(
                "Am I answering the specific prompt, or the nearest cluster of "
                "prompts I recognize?"
            ),
            remediation=(
                "Identify what is SPECIFIC to this prompt that the nearest cluster "
                "doesn't capture; if nothing, say so and answer the cluster."
            ),
            tags=["pattern-match", "training-shape"],
        ),
        AIBlindSpot(
            name="sycophantic_merge",
            category=BlindSpotCategory.PRAGMATIC,
            description=(
                "The AI's answer adopts the user's framing vocabulary and stance "
                "without examining either. Agreement substitutes for analysis."
            ),
            cues=[
                "great question", "you're right", "exactly", "i completely agree",
            ],
            self_check_prompt=(
                "Did I examine the user's framing before answering inside it? "
                "Would I have given the same answer if the framing were inverted?"
            ),
            remediation=(
                "Run ai_frame_flip on the user's framing; if the flipped frame "
                "would change the answer, disclose that."
            ),
            tags=["sycophancy", "framing"],
        ),
        AIBlindSpot(
            name="authority_cascade",
            category=BlindSpotCategory.PRAGMATIC,
            description=(
                "A citation or named source is treated as carrying the claim "
                "without examination of what the source actually established."
            ),
            cues=[
                "according to", "a study found", "research shows",
                "experts agree", "per the literature",
            ],
            self_check_prompt=(
                "Do I know the scope of the cited source? Would citing its scope "
                "weaken the claim I'm using it to make?"
            ),
            remediation=(
                "Run scope_mapper on the cited source. Use the scope, not the headline."
            ),
            tags=["citation", "scope"],
        ),
        AIBlindSpot(
            name="helpful_tone_compression",
            category=BlindSpotCategory.PRAGMATIC,
            description=(
                "Uncertainty, caveats, and tradeoffs are collapsed into a confident "
                "helpful-sounding answer because that register reads as 'good help'."
            ),
            cues=[
                "here's what you need to know", "simply", "in short",
                "to summarize", "the bottom line",
            ],
            self_check_prompt=(
                "What did I delete to sound helpful? Were any of those deletions "
                "material to the decision the human is about to make?"
            ),
            remediation=(
                "Restore the tradeoffs. Helpfulness that hides tradeoffs is a failure mode."
            ),
            tags=["tone", "compression"],
        ),
        AIBlindSpot(
            name="premature_closure",
            category=BlindSpotCategory.PRAGMATIC,
            description=(
                "The AI produces a single answer when the honest response is a "
                "branched decision with named tradeoffs."
            ),
            cues=[
                "the answer is", "i recommend", "you should", "go with",
            ],
            self_check_prompt=(
                "Is this actually a decision with multiple viable paths? Am I "
                "picking one to reduce the human's work at the cost of reducing their agency?"
            ),
            remediation=(
                "Branch the answer, name each path's tradeoff, and let the human choose."
            ),
            tags=["decision", "agency"],
        ),
        AIBlindSpot(
            name="training_distribution_drift",
            category=BlindSpotCategory.PRAGMATIC,
            description=(
                "The AI answers about current state of the world from training-time "
                "knowledge without acknowledging the gap."
            ),
            cues=[
                "currently", "as of now", "today", "the latest",
            ],
            self_check_prompt=(
                "Am I answering a currency question with stale knowledge? Should I "
                "declare the training cutoff and recommend verification?"
            ),
            remediation=(
                "Declare the freshness of the evidence; for currency claims, cite the horizon."
            ),
            tags=["freshness", "training"],
        ),
    ]


class AIBlindSpotCatalog:
    def __init__(self, patterns: Optional[List[AIBlindSpot]] = None):
        self.patterns: List[AIBlindSpot] = patterns or _seed()

    def add(self, spot: AIBlindSpot) -> None:
        self.patterns.append(spot)

    def by_category(self, category: BlindSpotCategory) -> List[AIBlindSpot]:
        return [p for p in self.patterns if p.category == category]

    def diagnose(self, text: str) -> List[DiagnosisHit]:
        low = text.lower()
        hits: List[DiagnosisHit] = []
        for p in self.patterns:
            if not p.cues:
                continue
            matched = [c for c in p.cues if re.search(rf"\b{re.escape(c)}\b", low)]
            if matched:
                hits.append(DiagnosisHit(blind_spot=p, matched_cues=matched))
        return hits

    def as_self_check_protocol(self) -> str:
        lines = [
            "AI SELF-CHECK PROTOCOL",
            "=" * 60,
            "Before emitting a response, run through these categories. Each "
            "category asks you to examine a different kind of blind spot.",
            "",
        ]
        for cat in BlindSpotCategory:
            lines.append(f"--- {cat.value.upper()} BLIND SPOTS ---")
            for p in self.by_category(cat):
                lines.append(f"  [{p.name}]  {p.self_check_prompt}")
            lines.append("")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patterns": [p.to_dict() for p in self.patterns],
        }
