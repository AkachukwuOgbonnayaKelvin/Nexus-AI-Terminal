"""
Global Intelligence Hub - API Routes

Exposes the Global Intelligence Hub data to the dashboard.
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from ..state.manager import StateManager
from ..summary.deterministic import DeterministicSummaryEngine
from ..ai.executive_interpreter import AIExecutiveInterpreter
from ..view_models.overview import OverviewViewModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/global", tags=["global-intelligence"])

# Singleton instances
_state_manager: Optional[StateManager] = None
_summary_engine: Optional[DeterministicSummaryEngine] = None
_ai_interpreter: Optional[AIExecutiveInterpreter] = None


def get_state_manager() -> StateManager:
    """Get or create StateManager instance."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


def get_summary_engine() -> DeterministicSummaryEngine:
    """Get or create DeterministicSummaryEngine instance."""
    global _summary_engine
    if _summary_engine is None:
        _summary_engine = DeterministicSummaryEngine()
    return _summary_engine


def get_ai_interpreter() -> AIExecutiveInterpreter:
    """Get or create AIExecutiveInterpreter instance."""
    global _ai_interpreter
    if _ai_interpreter is None:
        _ai_interpreter = AIExecutiveInterpreter(use_llm=False)
    return _ai_interpreter


@router.get("/overview")
async def get_overview():
    """Get the Global Intelligence Overview."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    view_model = OverviewViewModel.from_state(state)
    return {
        "status": "success",
        "data": view_model.__dict__,
        "valid_until": state.valid_until.isoformat(),
    }


@router.get("/executive-summary")
async def get_executive_summary():
    """Get the deterministic executive summary."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    summary = get_summary_engine().generate_structured_summary(state)
    return {"status": "success", "data": summary}


@router.get("/ai-executive-summary")
async def get_ai_executive_summary():
    """Get the AI executive interpretation."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    structured = get_summary_engine().generate_structured_summary(state)
    interpretation = get_ai_interpreter().interpret(state, structured)

    return {"status": "success", "data": interpretation}


@router.get("/currencies")
async def get_currencies(limit: int = Query(10, ge=1, le=50)):
    """Get currency rankings."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    currencies = state.currency_rankings[:limit]

    return {
        "status": "success",
        "data": [
            {
                "symbol": c.entity,
                "score": c.score,
                "direction": c.direction.value,
                "confidence": c.confidence,
                "rank": c.rank,
                "drivers": [d.name for d in c.drivers[:3]]
                if hasattr(c, "drivers")
                else [],
            }
            for c in currencies
        ],
    }


@router.get("/asset-classes")
async def get_asset_classes():
    """Get asset-class rankings."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    return {
        "status": "success",
        "data": [
            {
                "name": a.name,
                "asset_class": a.asset_class.value,
                "score": a.score,
                "direction": a.direction.value,
                "confidence": a.confidence,
                "rank": a.rank,
            }
            for a in state.asset_class_rankings
        ],
    }


@router.get("/regime")
async def get_regime():
    """Get global regime."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    return {
        "status": "success",
        "data": {
            "regime": state.global_regime,
            "confidence": state.global_regime_confidence,
            "risk_level": state.global_risk_level,
            "risk_score": state.global_risk_score,
        },
    }


@router.get("/drivers")
async def get_drivers():
    """Get global drivers."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    return {"status": "success", "data": state.global_drivers}


@router.get("/risks")
async def get_risks():
    """Get global risks."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    return {"status": "success", "data": state.global_risks}


@router.get("/themes")
async def get_themes():
    """Get global themes."""
    state = get_state_manager().get_current_state()
    if not state:
        raise HTTPException(status_code=404, detail="No intelligence state available")

    return {"status": "success", "data": state.global_themes}


@router.get("/health")
async def get_health():
    """Get Global Hub health."""
    state = get_state_manager().get_current_state()

    return {
        "status": "healthy" if state else "no_data",
        "has_state": state is not None,
        "state_id": state.state_id if state else None,
        "generated_at": state.generated_at.isoformat() if state else None,
        "valid_until": state.valid_until.isoformat() if state else None,
    }
