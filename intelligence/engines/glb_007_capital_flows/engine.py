"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Main Engine
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from .constants import NDIP_TOPICS
from .input.schemas import CapitalFlowInput, LiquidityInput
from .input.data_normalizer import DataNormalizer
from .analysis.flow_analyzer import FlowAnalyzer
from .liquidity.liquidity_analyzer import LiquidityAnalyzer
from .impact.asset_impact_matrix import AssetImpactMatrixGenerator

logger = logging.getLogger(__name__)


class CapitalFlowsEngine:
    """
    GLB-007 Capital Flows & Liquidity Intelligence Engine
    
    Analyzes capital flows and liquidity conditions and produces:
    1. Core Intelligence: Flow and liquidity analysis
    2. Asset Impact Matrix: How flows and liquidity affect assets
    """
    
    def __init__(self):
        self.data_normalizer = DataNormalizer()
        self.flow_analyzer = FlowAnalyzer()
        self.liquidity_analyzer = LiquidityAnalyzer()
        
        self.last_report: Optional[Dict] = None
        self.last_run_time: Optional[datetime] = None
        self._latest_data: Dict[str, Any] = {}
    
    def consume_ndip(self, topic: str, payload: Dict[str, Any]) -> None:
        """Consume NDIP contract."""
        self._latest_data[topic] = payload
    
    def run(self) -> Dict[str, Any]:
        """Run the engine analysis."""
        start_time = time.time()
        
        # 1. Parse and normalize flows
        flows = self._parse_flows()
        
        # 2. Parse and normalize liquidity
        liquidity = self._parse_liquidity()
        
        if not flows:
            return self._empty_report()
        
        # 3. Analyze flows
        flow_analysis = self.flow_analyzer.analyze_flows(flows)
        
        # 4. Analyze liquidity
        liquidity_analysis = self.liquidity_analyzer.analyze_liquidity(liquidity)
        
        # 5. Build core intelligence
        core_intelligence = self._build_core_intelligence(flow_analysis, liquidity_analysis)
        
        # 6. Generate asset impact matrix
        impact_matrix = AssetImpactMatrixGenerator.generate(
            flow_analysis, liquidity_analysis, core_intelligence["confidence"]
        )
        
        # 7. Build final report
        report = {
            "engine_id": "GLB-007",
            "engine_name": "Capital Flows & Liquidity Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": core_intelligence,
            "asset_impact_matrix": impact_matrix.model_dump() if impact_matrix else None,
            "metadata": {
                "calculation_time_ms": int((time.time() - start_time) * 1000),
                "flow_count": len(flows),
                "model_version": "1.0.0"
            }
        }
        
        self.last_report = report
        self.last_run_time = datetime.utcnow()
        
        logger.info(f"GLB-007 completed: {len(flows)} flows analyzed")
        
        return report
    
    def _parse_flows(self) -> List[CapitalFlowInput]:
        """Parse flows from NDIP data."""
        flows_data = self._latest_data.get(NDIP_TOPICS["CAPITAL_FLOWS"], {})
        raw_flows = flows_data.get("flows", [])
        
        parsed = []
        for raw in raw_flows:
            normalized = self.data_normalizer.normalize_flow(raw)
            if normalized:
                parsed.append(normalized)
        
        return parsed
    
    def _parse_liquidity(self) -> Optional[LiquidityInput]:
        """Parse liquidity from NDIP data."""
        liquidity_data = self._latest_data.get(NDIP_TOPICS["GLOBAL_LIQUIDITY"], {})
        if not liquidity_data:
            return None
        return self.data_normalizer.normalize_liquidity(liquidity_data)
    
    def _build_core_intelligence(self, flow_analysis: Dict, liquidity_analysis: Dict) -> Dict:
        """Build core intelligence report"""
        return {
            "global_flow_state": flow_analysis.get("dominant_flow", "UNKNOWN"),
            "capital_flow_score": flow_analysis.get("flow_strength", 0),
            "flow_direction": flow_analysis.get("flow_direction", "NEUTRAL"),
            "flow_momentum": flow_analysis.get("momentum", "STABLE"),
            "liquidity_score": liquidity_analysis.get("liquidity_score", 50),
            "liquidity_state": liquidity_analysis.get("liquidity_state", "NORMAL"),
            "funding_stress": liquidity_analysis.get("funding_stress", 50),
            "net_flow": flow_analysis.get("net_flow", 0),
            "total_inflows": flow_analysis.get("total_inflow", 0),
            "total_outflows": flow_analysis.get("total_outflow", 0),
            "asset_class_flows": flow_analysis.get("asset_class_flows", {}),
            "flow_count": flow_analysis.get("flow_count", 0),
            "confidence": flow_analysis.get("confidence", 50.0),
        }
    
    def _empty_report(self) -> Dict:
        """Return empty report when no flows."""
        return {
            "engine_id": "GLB-007",
            "engine_name": "Capital Flows & Liquidity Intelligence Engine",
            "version": "1.0.0",
            "status": "OPERATIONAL",
            "generated_at": datetime.utcnow().isoformat(),
            "core_intelligence": {
                "global_flow_state": "UNKNOWN",
                "capital_flow_score": 0,
                "flow_direction": "NEUTRAL",
                "flow_momentum": "STABLE",
                "liquidity_score": 50,
                "liquidity_state": "NORMAL",
                "funding_stress": 50,
                "flow_count": 0,
                "confidence": 50.0
            },
            "asset_impact_matrix": None,
            "metadata": {"flow_count": 0}
        }
    
    def get_last_report(self) -> Optional[Dict]:
        return self.last_report
    
    def health_check(self) -> Dict[str, Any]:
        return {
            "engine_id": "GLB-007",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_report": self.last_report is not None
        }
