import logging
from typing import Any, Dict

from ndip.reference_data.audit_manager import AuditManager
from ndip.reference_data.conflict_manager import ConflictManager
from ndip.reference_data.dependency_manager import DependencyManager
from ndip.reference_data.loaders import (
    AssetTypeLoader,
    CompanyLoader,
    CountryLoader,
    CurrencyLoader,
    ExchangeLoader,
    IndustryLoader,
    SectorLoader,
)
from ndip.reference_data.quality_manager import QualityManager
from ndip.reference_data.registry_manager import RegistryManager
from ndip.reference_data.version_manager import VersionManager

logger = logging.getLogger(__name__)


class ReferenceDataManager:
    def __init__(self):
        self.registry_manager = RegistryManager()
        self.dependency_manager = DependencyManager()
        self.conflict_manager = ConflictManager()
        self.version_manager = VersionManager()
        self.quality_manager = QualityManager()
        self.audit_manager = AuditManager()
        self.loaders = {
            "exchange": ExchangeLoader(self.registry_manager),
            "currency": CurrencyLoader(self.registry_manager),
            "country": CountryLoader(self.registry_manager),
            "sector": SectorLoader(self.registry_manager),
            "industry": IndustryLoader(self.registry_manager),
            "company": CompanyLoader(self.registry_manager),
            "asset_type": AssetTypeLoader(self.registry_manager),
        }

    async def resolve_asset(self, metadata: Dict[str, Any], source: str) -> Dict[str, Any]:
        refs = self._extract_references(metadata)
        resolved = {}
        for ref_type in self.dependency_manager.get_order():
            value = refs.get(ref_type)
            if value:
                canonical = self.conflict_manager.resolve(ref_type, value)
                loader = self.loaders.get(ref_type)
                if loader:
                    resolved_id = await loader.ensure(canonical, source, metadata)
                    if resolved_id:
                        resolved[ref_type] = resolved_id

        asset_record = metadata.copy()
        for ref_type, ref_id in resolved.items():
            column_name = self.dependency_manager.get_column(ref_type)
            asset_record[column_name] = ref_id

        for ref_type in self.dependency_manager.get_order():
            if ref_type in asset_record:
                del asset_record[ref_type]

        asset_record["quality_score"] = self.quality_manager.score(metadata, source)
        asset_record["provider"] = source
        asset_record["provider_rank"] = self.quality_manager.get_provider_rank(source)

        return asset_record

    def _extract_references(self, metadata: dict) -> dict:
        return {
            "exchange": metadata.get("exchange_code") or metadata.get("exchange"),
            "currency": metadata.get("base_currency") or metadata.get("currency"),
            "country": metadata.get("country"),
            "sector": metadata.get("sector"),
            "industry": metadata.get("industry"),
            "company": metadata.get("company_name") or metadata.get("company"),
            "asset_type": metadata.get("instrument_type"),
        }
