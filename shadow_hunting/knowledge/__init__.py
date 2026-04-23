"""Knowledge liberation pipeline — scope mapping, edge exploration, application building.

Imported from JinnZ2/Logic-Ferret (CC0). The pipeline clarifies what a study
actually measured, probes the edges of its scope, and names legitimate uses
alongside misapplications to avoid.

Core pipeline: scope_mapper -> edge_explorer -> application_builder
Playground:    interactive_navigator, shadow_catalog, recontextualizer
"""

from .scope_mapper import ScopeMapper, ScopeMap, MeasurementType, SelectionType, map_scope
from .edge_explorer import EdgeExplorer, EdgeQuestion, EdgeExploration, EdgeType
from .application_builder import (
    ApplicationBuilder,
    LegitimateApplication,
    Misapplication,
    BuildPlan,
    ApplicationDomain,
)
from .knowledge_liberation import StudyInput, liberate
from .shadow_catalog import ShadowCatalog
from .recontextualizer import (
    UserContext,
    ContextRole,
    recontextualize_silences,
)
from .interactive_navigator import Navigator

from .ai_provenance import Provenance, TaggedClaim
from .ai_claim_decomposer import (
    ClaimLayer,
    DecomposedClaim,
    decompose,
    decompose_as_prompt,
)
from .ai_frame_flip import FlipAxis, FrameFlip, FrameFlipReport, flip_frame
from .ai_self_scope import (
    ReasoningMode,
    ConfidenceTier,
    SelfScope,
    self_scope,
)
from .ai_blind_spots import (
    BlindSpotCategory,
    AIBlindSpot,
    AIBlindSpotCatalog,
    DiagnosisHit,
)
from .ai_brief import (
    ScopeBrief,
    EdgeBrief,
    BuildBrief,
    StudyAIBrief,
    scope_brief,
    edge_brief,
    build_brief,
    ai_brief,
)
from .ai_critical_thinking import CriticalThinkingReport, check_response

__all__ = [
    "ScopeMapper",
    "ScopeMap",
    "MeasurementType",
    "SelectionType",
    "map_scope",
    "EdgeExplorer",
    "EdgeQuestion",
    "EdgeExploration",
    "EdgeType",
    "ApplicationBuilder",
    "LegitimateApplication",
    "Misapplication",
    "BuildPlan",
    "ApplicationDomain",
    "StudyInput",
    "liberate",
    "ShadowCatalog",
    "UserContext",
    "ContextRole",
    "recontextualize_silences",
    "Navigator",
    "Provenance",
    "TaggedClaim",
    "ClaimLayer",
    "DecomposedClaim",
    "decompose",
    "decompose_as_prompt",
    "FlipAxis",
    "FrameFlip",
    "FrameFlipReport",
    "flip_frame",
    "ReasoningMode",
    "ConfidenceTier",
    "SelfScope",
    "self_scope",
    "BlindSpotCategory",
    "AIBlindSpot",
    "AIBlindSpotCatalog",
    "DiagnosisHit",
    "ScopeBrief",
    "EdgeBrief",
    "BuildBrief",
    "StudyAIBrief",
    "scope_brief",
    "edge_brief",
    "build_brief",
    "ai_brief",
    "CriticalThinkingReport",
    "check_response",
]
