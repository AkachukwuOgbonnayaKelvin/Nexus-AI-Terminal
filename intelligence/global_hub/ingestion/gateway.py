"""
Global Intelligence Hub - Ingestion Gateway

The front door of the Global Intelligence Hub.
Receives and validates Confluence output.
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from ...confluence.contracts import GlobalIntelligenceOutput
from ...confluence.distribution.validator import OutputValidator

logger = logging.getLogger(__name__)


class IngestionGateway:
    """
    Ingestion Gateway for the Global Intelligence Hub.

    Responsibilities:
    - Receive GlobalIntelligenceOutput
    - Validate schema
    - Validate freshness
    - Validate status = FINAL
    - Validate rank integrity
    - Prevent duplicates
    - Pass valid data to State Manager
    - REJECT invalid data
    """

    def __init__(self, strict_validation: bool = True):
        self.validator = OutputValidator()
        self._processed_ids: set = set()
        self._last_ingestion: datetime | None = None
        self.strict_validation = strict_validation

    def ingest(self, output: GlobalIntelligenceOutput) -> dict[str, Any]:
        """
        Ingest a GlobalIntelligenceOutput.

        Args:
            output: GlobalIntelligenceOutput from Confluence

        Returns:
            Dict with status and validation results
        """
        logger.info("Ingesting GlobalIntelligenceOutput...")

        # Step 1: Validate schema
        validation = self.validator.validate_global_output(output)
        if not validation.valid:
            logger.error(f"Validation failed: {validation.errors}")
            return {
                "status": "rejected",
                "reason": "validation_failed",
                "errors": validation.errors,
                "warnings": validation.warnings,
            }

        # Step 2: Validate rank integrity
        rank_validation = self._validate_rank_integrity(output)
        if not rank_validation["valid"]:
            logger.error(f"Rank validation failed: {rank_validation['errors']}")
            return {
                "status": "rejected",
                "reason": "rank_integrity_failed",
                "errors": rank_validation["errors"],
                "details": rank_validation["details"],
            }

        # Step 3: Check freshness
        timestamp = getattr(output, "timestamp", None)
        if timestamp:
            age = datetime.utcnow() - timestamp
            if age > timedelta(hours=2):
                logger.warning(f"Output is stale: {age}")
                if self.strict_validation:
                    return {
                        "status": "rejected",
                        "reason": "stale_output",
                        "age_seconds": age.total_seconds(),
                        "max_age_hours": 2,
                    }
                else:
                    return {
                        "status": "warning",
                        "reason": "stale_output",
                        "age_seconds": age.total_seconds(),
                        "max_age_hours": 2,
                    }

        # Step 4: Check for duplicates
        output_id = getattr(output, "state_id", None)
        if output_id and output_id in self._processed_ids:
            logger.warning(f"Duplicate output: {output_id}")
            return {"status": "warning", "reason": "duplicate", "output_id": output_id}

        # Step 5: Record ingestion
        if output_id:
            self._processed_ids.add(output_id)
        self._last_ingestion = datetime.utcnow()

        logger.info("Ingestion successful")
        return {
            "status": "accepted",
            "validation": {"valid": validation.valid, "warnings": validation.warnings},
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _validate_rank_integrity(
        self, output: GlobalIntelligenceOutput
    ) -> dict[str, Any]:
        """
        Validate that all rankings have sequential ranks starting from 1.

        Returns:
            Dict with valid flag, errors, and details
        """
        errors = []
        details = {}

        # Check currency rankings
        if output.currency_rankings:
            ranks = [r.rank for r in output.currency_rankings if r.rank is not None]
            if ranks:
                expected = list(range(1, len(ranks) + 1))
                if ranks != expected:
                    errors.append(f"Currency rankings: {ranks} vs expected {expected}")
                    details["currency_rankings"] = {
                        "actual": ranks,
                        "expected": expected,
                    }

        # Check entity rankings
        if output.entity_rankings:
            ranks = [r.rank for r in output.entity_rankings if r.rank is not None]
            if ranks:
                expected = list(range(1, len(ranks) + 1))
                if ranks != expected:
                    errors.append(f"Entity rankings: {ranks} vs expected {expected}")
                    details["entity_rankings"] = {"actual": ranks, "expected": expected}

        # Check asset-class rankings
        if output.asset_class_rankings:
            ranks = [r.rank for r in output.asset_class_rankings if r.rank is not None]
            if ranks:
                expected = list(range(1, len(ranks) + 1))
                if ranks != expected:
                    errors.append(
                        f"Asset-class rankings: {ranks} vs expected {expected}"
                    )
                    details["asset_class_rankings"] = {
                        "actual": ranks,
                        "expected": expected,
                    }

        return {"valid": len(errors) == 0, "errors": errors, "details": details}

    def get_last_ingestion(self) -> datetime | None:
        """Get the last successful ingestion time."""
        return self._last_ingestion

    def reset(self) -> None:
        """Reset the ingestion gateway."""
        self._processed_ids.clear()
        self._last_ingestion = None
