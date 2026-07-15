"""NDIP Gateway implementation."""

from datetime import datetime
from typing import Any, Dict

from ndip.classification import Classifier
from ndip.normalization import Normalizer
from ndip.validation import Validator
from ndip.warehouse import Warehouse


class DataGateway:
    """Data Gateway - Entry point for all external data."""

    def __init__(self) -> None:
        self.validator = Validator()
        self.normalizer = Normalizer()
        self.classifier = Classifier()
        self.warehouse = Warehouse()
        self._sources: Dict[str, Any] = {}
        self._stats: Dict[str, Any] = {
            "total_records": 0,
            "last_ingest": None,
            "errors": 0,
        }

    def register_source(self, name: str, source: Any) -> None:
        """Register a data source."""
        self._sources[name] = source

    def ingest(self, source: str, data: Any) -> Dict[str, Any]:
        """Ingest data from a source."""
        try:
            # Validate
            validated = self.validator.validate(data)

            # Normalize
            normalized = self.normalizer.normalize(validated)

            # Classify
            classified = self.classifier.classify(normalized)

            # Store
            self.warehouse.store(classified, source)

            # Update stats
            self._stats["total_records"] += 1
            self._stats["last_ingest"] = datetime.now()

            return {
                "success": True,
                "source": source,
                "records": len(data) if isinstance(data, list) else 1,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self._stats["errors"] += 1
            return {
                "success": False,
                "source": source,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get gateway statistics."""
        return self._stats
