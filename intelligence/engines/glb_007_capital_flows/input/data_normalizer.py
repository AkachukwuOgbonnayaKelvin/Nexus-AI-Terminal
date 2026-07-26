"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Data Normalizer
"""

import logging
from datetime import datetime
from typing import Any

from ..constants import CapitalFlowType, FlowDirection
from .schemas import CapitalFlowInput, LiquidityInput

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Normalize raw NDIP data into canonical format"""

    def normalize_flow(self, raw: dict[str, Any]) -> CapitalFlowInput | None:
        """Normalize a raw flow record"""
        try:
            return CapitalFlowInput(
                flow_id=raw.get("flow_id", f"FLOW_{datetime.utcnow().timestamp()}"),
                asset=raw.get("asset", "UNKNOWN"),
                region=raw.get("region", "GLOBAL"),
                flow_type=CapitalFlowType(raw.get("flow_type", "RISK_ON")),
                direction=FlowDirection(raw.get("direction", "NEUTRAL")),
                amount=raw.get("amount", 0.0),
                amount_normalized=raw.get("amount_normalized", 50.0),
                velocity=raw.get("velocity", 50.0),
                persistence=raw.get("persistence", 50.0),
                confidence=raw.get("confidence", 70.0),
                timestamp=datetime.fromisoformat(
                    raw.get("timestamp", datetime.utcnow().isoformat())
                ),
                source=raw.get("source", "NDIP"),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize flow: {e}")
            return None

    def normalize_liquidity(self, raw: dict[str, Any]) -> LiquidityInput | None:
        """Normalize raw liquidity data"""
        try:
            return LiquidityInput(
                global_liquidity=raw.get("global_liquidity", 50.0),
                central_bank_liquidity=raw.get("central_bank_liquidity", 50.0),
                money_market_liquidity=raw.get("money_market_liquidity", 50.0),
                credit_liquidity=raw.get("credit_liquidity", 50.0),
                funding_stress=raw.get("funding_stress", 50.0),
                confidence=raw.get("confidence", 70.0),
                timestamp=datetime.fromisoformat(
                    raw.get("timestamp", datetime.utcnow().isoformat())
                ),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize liquidity: {e}")
            return None
