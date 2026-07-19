"""Parser Factory – Routes to the correct parser based on report type."""

import logging
from typing import Any, Dict, List

from institutional_positioning_engine.parser.disaggregated import DisaggregatedParser
from institutional_positioning_engine.parser.legacy import LegacyParser
from institutional_positioning_engine.parser.tff import TFFParser

logger = logging.getLogger(__name__)


class ParserFactory:
    """Factory that returns the correct parser based on report type."""

    def __init__(self):
        self.parsers = {
            "disaggregated": DisaggregatedParser(),
            "legacy": LegacyParser(),
            "tff": TFFParser(),
        }
        self._default_parser = DisaggregatedParser()

    def get_parser(self, report_type: str):
        """Get the appropriate parser for the report type."""
        parser = self.parsers.get(report_type.lower())
        if not parser:
            logger.warning(f"Unknown report type: {report_type}, using default parser")
            return self._default_parser
        return parser

    def parse(self, report_type: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse data using the correct parser."""
        parser = self.get_parser(report_type)
        logger.info(f"Parsing {len(data)} records with {parser.get_report_type()} parser")
        return parser.parse(data)

    def get_supported_types(self) -> List[str]:
        """Get list of supported report types."""
        return list(self.parsers.keys())
