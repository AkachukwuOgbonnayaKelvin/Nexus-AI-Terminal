"""Master acquisition coordinator."""

from typing import Any, Dict

from ndip.normalization.normalizer import Normalizer
from ndip.publication.router import PublicationRouter
from ndip.validation.validator import Validator


class AcquisitionCollector:
    """Coordinates data acquisition from providers."""

    def __init__(self):
        self.validator = Validator()
        self.normalizer = Normalizer()
        self.router = PublicationRouter()
        self.providers = {}

    def register_provider(self, name: str, provider):
        self.providers[name] = provider

    async def ingest(self, source: str, data: Any) -> Dict[str, Any]:
        """Process incoming data through the NDIP pipeline."""
        try:
            # Validate
            validated = self.validator.validate(data)
            # Normalize
            normalized = self.normalizer.normalize(validated)
            # Route to warehouse via publication
            if "records" in normalized:
                results = []
                for rec in normalized["records"]:
                    res = await self.router.route(rec, source)
                    results.append(res)
                return {"success": True, "records": results}
            elif "record" in normalized:
                result = await self.router.route(normalized["record"], source)
                return {"success": True, "record": result}
            else:
                return {"success": False, "error": "No records found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
