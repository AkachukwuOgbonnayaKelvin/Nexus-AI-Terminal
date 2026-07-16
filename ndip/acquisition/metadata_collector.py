import logging
from typing import Any, Dict, List

from ndip.normalization.metadata_normalizer import MetadataNormalizer
from ndip.reference_data.manager import ReferenceDataManager
from ndip.validation.metadata_validator import MetadataValidator
from ndip.warehouses.metadata_warehouse import MetadataWarehouse

logger = logging.getLogger(__name__)


class MetadataAcquisitionCollector:
    def __init__(self, provider_manager):
        self.provider_manager = provider_manager
        self.warehouse = MetadataWarehouse()
        self.validator = MetadataValidator()
        self.normalizer = MetadataNormalizer()
        self.rdm = ReferenceDataManager()

    async def collect(self, symbols: List[str]) -> Dict[str, Any]:
        results = {}
        for symbol in symbols:
            found = False
            for provider_name in self.provider_manager.health.get_priority_order(asset_class=None):
                provider = self.provider_manager.providers.get(provider_name)
                if not provider or not hasattr(provider, "get_metadata"):
                    continue
                if not self.provider_manager.health.is_healthy(provider_name):
                    continue
                try:
                    raw = provider.get_metadata(symbol)
                    if not isinstance(raw, dict):
                        logger.warning(f"Provider {provider_name} returned non-dict for {symbol}: {type(raw)}")
                        continue
                    validated = self.validator.validate(raw)
                    normalized = self.normalizer.normalize(validated)
                    # Resolve references using RDM
                    resolved = await self.rdm.resolve_asset(normalized, provider_name)
                    # Store asset
                    result = await self.warehouse.store_asset(resolved, provider_name)
                    results[symbol] = {
                        "status": "success",
                        "provider": provider_name,
                        "details": result,
                    }
                    found = True
                    break
                except Exception as e:
                    logger.warning(f"Provider {provider_name} failed for {symbol}: {e}")
                    continue
            if not found:
                results[symbol] = {"status": "failed", "error": "No provider available"}
        return results
