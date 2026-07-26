"""Parser Factory – Creates appropriate parser for data."""

import logging
from datetime import datetime
from typing import Any

from market_positioning_warehouse.dtos import UniversalPosition

logger = logging.getLogger(__name__)


class ParserFactory:
    """Factory for creating parsers."""

    def parse(self, data: list[dict[str, Any]]) -> list[UniversalPosition]:
        """Parse raw data into UniversalPosition objects."""
        positions = []
        for item in data:
            try:
                position = UniversalPosition(
                    market_name=item.get("market_name", "Unknown"),
                    report_date=datetime.now(),
                    source="parsed",
                )
                positions.append(position)
            except Exception as e:
                logger.warning(f"Failed to parse item: {e}")
        logger.info(f"Parsed {len(positions)} positions")
        return positions
