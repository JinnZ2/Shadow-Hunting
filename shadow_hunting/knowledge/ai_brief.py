"""Provenance-tagged JSON layer over the knowledge pipeline.

The prose output of scope_mapper / edge_explorer / application_builder is
written for humans. For AI consumption we want JSON where every element is
tagged so the AI can tell user-supplied content from template-universal
scaffolding from heuristic-triggered matches.

This keeps the AI honest: it will not present "edge 6: adaptation reframe"
as a discovery, because the AI brief marks it TEMPLATE_UNIVERSAL — i.e. it
fires for every input. But "silence: undergraduate population" shows up as
HEURISTIC_TRIGGERED with trigger 'keyword:student' so the AI knows this
particular flag actually matched the user's inputs.

License: CC0
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from .scope_mapper import ScopeMapper
from .edge_explorer import EdgeExplorer
from .application_builder import ApplicationBuilder
from .knowledge_liberation import StudyInput
from .ai_provenance import TaggedClaim, Provenance, user, template, heuristic, derived


_SHORT_DURATIONS = ("minute", "hour", "single session", "day", "week")
_LAB_TOKENS = ("lab",)
_STUDENT_TOKENS = ("student", "undergraduate")
_SURVIVAL_TOKENS = ("trauma", "adversity", "stress", "threat")
_RESPONSE_TOKENS = ("response", "reactivity")


def _tag_scope_silences(
    claim: str,
    measured: str,
    pop: str,
    env: str,
    dur: str,
    uncontrolled: List[str],
) -> List[TaggedClaim]:
    out: List[TaggedClaim] = []

    for tok in _SHORT_DURATIONS:
        if tok in dur.lower():
            out.append(heuristic(
                content=f"What happens over longer time scales beyond the {dur} measurement window?",
                trigger=f"duration_contains:{tok}",
                source_fields=["duration"],
            ))
            break

    for tok in _LAB_TOKENS:
        if tok in env.lower():
            out.append(heuristic(
                content="Does the finding replicate in field/real-world conditions where uncontrolled variables are present?",
                trigger=f"environment_contains:{tok}",
                source_fields=["environment"],
            ))
            break

    for tok in _STUDENT_TOKENS:
        if tok in pop.lower():
            out.append(heuristic(
                content="Does the finding generalize to populations with different life history, body composition, or environmental exposure?",
                trigger=f"population_contains:{tok}",
                source_fields=["population"],
            ))
            break

    for tok in _SURVIVAL_TOKENS:
        if tok in claim.lower():
            out.append(heuristic(
                content="How do SURVIVORS of the same condition compare — they may have been recalibrated by experience?",
                trigger=f"claim_contains:{tok}",
                source_fields=["claimed_finding"],
            ))
            out.append(heuristic(
                content="Could the measured state be an ADAPTATION rather than an impairment?",
                trigger=f"claim_contains:{tok}",
                source_fields=["claimed_finding"],
            ))
            break

    for var in uncontrolled:
        out.append(derived(
            content=f"The study did not control for {var}. What is the finding's dependence on that variable?",
            source_fields=["uncontrolled_variables"],
            note="one entry per uncontrolled variable",
        ))

    for tok in _RESPONSE_TOKENS:
        if tok in measured.lower():
            out.append(heuristic(
                content="Was this measuring IMPAIRMENT or INCREASED TOLERANCE / RECALIBRATION? The instrument may not distinguish.",
                trigger=f"measurement_contains:{tok}",
                source_fields=["what_was_measured"],
            ))
            break

    return out


@dataclass
class ScopeBrief:
    inputs: Dict[str, Any]
    load_bearing_claim: TaggedClaim
    applies_when: List[TaggedClaim]
    silent_when: List[TaggedClaim]
    silent_on: List[TaggedClaim]
    heuristic_fingerprint: Dict[str, List[str]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inputs": self.inputs,
            "load_bearing_claim": self.load_bearing_claim.to_dict(),
            "applies_when": [c.to_dict() for c in self.applies_when],
            "silent_when": [c.to_dict() for c in self.silent_when],
            "silent_on": [c.to_dict() for c in self.silent_on],
            "heuristic_fingerprint": self.heuristic_fingerprint,
        }


def scope_brief(study: StudyInput) -> ScopeBrief:
    mapper = ScopeMapper()
    scope = mapper.map_study(
        claimed_finding=study.claimed_finding,
        what_was_measured=study.what_was_measured,
        measurement_instrument=study.measurement_instrument,
        population=study.population,
        population_size=study.population_size,
        environment=study.environment,
        duration=study.duration,
        controlled=study.controlled_variables,
        uncontrolled=study.uncontrolled_variables,
    )

    applies_when: List[TaggedClaim] = []
    applies_when.append(derived(
        content=f"The population matches: {study.population}",
        source_fields=["population"],
    ))
    applies_when.append(derived(
        content=f"The environment is similar to: {study.environment}",
        source_fields=["environment"],
    ))
    applies_when.append(derived(
        content=f"The time scale is comparable to: {study.duration}",
        source_fields=["duration"],
    ))
    for var in study.controlled_variables:
        applies_when.append(derived(
            content=f"{var} is held at similar levels",
            source_fields=["controlled_variables"],
        ))

    silent_when: List[TaggedClaim] = []
    silent_when.append(derived(
        content=f"Population differs substantially from: {study.population}",
        source_fields=["population"],
    ))
    silent_when.append(derived(
        content=f"Environment differs from: {study.environment}",
        source_fields=["environment"],
    ))
    silent_when.append(derived(
        content=f"Time scale exceeds: {study.duration}",
        source_fields=["duration"],
    ))
    for var in study.uncontrolled_variables:
        silent_when.append(derived(
            content=f"{var} varies outside the study's implicit range",
            source_fields=["uncontrolled_variables"],
        ))

    silent_on = _tag_scope_silences(
        study.claimed_finding,
        study.what_was_measured,
        study.population,
        study.environment,
        study.duration,
        study.uncontrolled_variables,
    )

    fingerprint: Dict[str, List[str]] = {}
    for s in silent_on:
        if s.provenance == Provenance.HEURISTIC_TRIGGERED and s.trigger:
            fingerprint.setdefault(s.trigger, []).extend(s.source_fields)

    return ScopeBrief(
        inputs={
            "claimed_finding": study.claimed_finding,
            "what_was_measured": study.what_was_measured,
            "measurement_instrument": study.measurement_instrument,
            "population": study.population,
            "population_size": study.population_size,
            "environment": study.environment,
            "duration": study.duration,
            "controlled_variables": list(study.controlled_variables),
            "uncontrolled_variables": list(study.uncontrolled_variables),
            "measurement_type": scope.measurement_type.value,
            "selection_method": scope.selection_method.value,
        },
        load_bearing_claim=derived(
            content=scope.load_bearing_claim,
            source_fields=["claimed_finding", "population", "environment", "duration", "what_was_measured"],
            note="composed from user inputs via f-string template",
        ),
        applies_when=applies_when,
        silent_when=silent_when,
        silent_on=silent_on,
        heuristic_fingerprint=fingerprint,
    )


@dataclass
class EdgeBrief:
    claim: str
    edges: List[TaggedClaim]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim": self.claim,
            "edges": [e.to_dict() for e in self.edges],
        }


def edge_brief(study: StudyInput) -> EdgeBrief:
    explorer = EdgeExplorer()
    exploration = explorer.explore(
        claim=study.claimed_finding,
        what_was_measured=study.what_was_measured,
        population=study.population,
        environment=study.environment,
        duration=study.duration,
        uncontrolled_variables=study.uncontrolled_variables,
    )
    edges = [
        template(
            content=q.question,
            note=f"edge_type={q.edge_type.value}; fires for every input",
        )
        for q in exploration.generated_questions
    ]
    return EdgeBrief(claim=study.claimed_finding, edges=edges)


@dataclass
class BuildBrief:
    claim: str
    legitimate_applications: List[TaggedClaim]
    misapplications: List[TaggedClaim]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim": self.claim,
            "legitimate_applications": [a.to_dict() for a in self.legitimate_applications],
            "misapplications": [m.to_dict() for m in self.misapplications],
        }


def build_brief(study: StudyInput) -> BuildBrief:
    builder = ApplicationBuilder()
    plan = builder.build(
        claim=study.claimed_finding,
        scope_population=study.population,
        scope_environment=study.environment,
        scope_duration=study.duration,
        what_was_measured=study.what_was_measured,
        uncontrolled_variables=study.uncontrolled_variables,
    )
    apps = [
        template(
            content=a.description,
            note=f"domain={a.domain.value}; template fires for every input",
        )
        for a in plan.legitimate_applications
    ]
    misapps = [
        heuristic(
            content=m.description,
            trigger="misapplication_template",
            source_fields=["claimed_finding", "population", "environment"],
        )
        for m in plan.misapplications_to_avoid
    ]
    return BuildBrief(claim=study.claimed_finding, legitimate_applications=apps, misapplications=misapps)


@dataclass
class StudyAIBrief:
    scope: ScopeBrief
    edges: EdgeBrief
    build: BuildBrief

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scope": self.scope.to_dict(),
            "edges": self.edges.to_dict(),
            "build": self.build.to_dict(),
        }


def ai_brief(study: StudyInput) -> StudyAIBrief:
    return StudyAIBrief(
        scope=scope_brief(study),
        edges=edge_brief(study),
        build=build_brief(study),
    )
