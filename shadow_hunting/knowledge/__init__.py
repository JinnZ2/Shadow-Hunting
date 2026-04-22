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
]
