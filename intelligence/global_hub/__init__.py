"""
Global Intelligence Hub

The Global Intelligence Hub receives certified Confluence output and
transforms it into a coherent, structured, historical, AI-interpreted
and GUI-ready global intelligence state.

It does NOT create new intelligence - it organizes and interprets
what the Confluence Engine has already produced.

Two Final Feeders:
1. GUI Presentation Feeder → Dashboard (read-only mirror)
2. Orchestrator Feeder → Master Orchestrator (decision context)
"""

from .state.manager import StateManager
from .state.state import GlobalHubState
from .ingestion.gateway import IngestionGateway
from .summary.deterministic import DeterministicSummaryEngine
from .ai.executive_interpreter import AIExecutiveInterpreter
from .view_models.overview import OverviewViewModel
from .presentation.gui_feeder import GUIPresentationFeeder
from .orchestration.orchestrator_feeder import OrchestratorFeeder

__all__ = [
    "StateManager",
    "GlobalHubState",
    "IngestionGateway",
    "DeterministicSummaryEngine",
    "AIExecutiveInterpreter",
    "OverviewViewModel",
    "GUIPresentationFeeder",
    "OrchestratorFeeder",
]
