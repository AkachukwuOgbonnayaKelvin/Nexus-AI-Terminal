"""COT Validator – validates COT data."""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class COTValidator:
    def validate(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a COT record."""
        required = ["report_id", "report_date", "market_code", "open_interest"]
        for field in required:
            if not record.get(field):
                logger.warning(f"Missing required field: {field}")
                return None
        return record
