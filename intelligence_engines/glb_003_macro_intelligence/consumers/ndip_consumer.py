# -*- coding: utf-8 -*-
"""NDIP Consumer for Macro Intelligence Engine"""

from typing import Dict, Any, List
import logging

from intelligence_engines.glb_003_macro_intelligence.engine import (
    MacroIntelligenceEngine,
)


logger = logging.getLogger(__name__)


class NDIPConsumer:
    """
    NDIP Consumer for GLB-003 Macro Intelligence Engine.

    This consumer subscribes to NDIP topics and feeds data to the engine.
    """

    def __init__(self):
        self.engine = MacroIntelligenceEngine()
        self.topics = self.engine.get_required_ndip_topics()

    def consume(self, ndip_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consume NDIP data and run the engine.

        Args:
            ndip_data: Dictionary with NDIP topics and their data

        Returns:
            EngineReport from the macro intelligence engine
        """
        # Extract relevant data
        engine_input = {}
        for topic in self.topics:
            if topic in ndip_data:
                engine_input[topic] = ndip_data[topic]

        # Run the engine
        report = self.engine.run(engine_input)

        logger.info(f"Macro Intelligence Engine produced report: {report.report_id}")

        return report.to_dict()

    def get_topics(self) -> List[str]:
        """Get the topics this consumer subscribes to"""
        return self.topics
