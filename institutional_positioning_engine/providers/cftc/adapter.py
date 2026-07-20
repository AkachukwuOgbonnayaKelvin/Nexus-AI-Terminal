from datetime import datetime
from typing import Any, Dict, List

from institutional_positioning_engine.dtos import UniversalCOTRecord


class CFTCAdapter:
    def adapt(
        self, raw: Dict[str, Any], provider_name: str
    ) -> List[UniversalCOTRecord]:
        """Convert raw CFTC data to UniversalCOTRecord list."""
        if not raw:
            return []
        report_date = raw.get("report_date")
        if isinstance(report_date, str):
            report_date = datetime.fromisoformat(report_date)
        records = []
        for market in raw.get("markets", []):
            records.append(
                UniversalCOTRecord(
                    report_id=raw.get("report_id"),
                    provider=provider_name,
                    report_date=report_date or datetime.now(),
                    market_code=market.get("market_code"),
                    market_name=market.get("market_name"),
                    asset_class=market.get("asset_class"),
                    currency=market.get("currency"),
                    exchange=market.get("exchange"),
                    open_interest=market.get("open_interest"),
                    dealer_long=market.get("dealer_long"),
                    dealer_short=market.get("dealer_short"),
                    dealer_spreading=market.get("dealer_spreading"),
                    asset_manager_long=market.get("asset_manager_long"),
                    asset_manager_short=market.get("asset_manager_short"),
                    asset_manager_spreading=market.get("asset_manager_spreading"),
                    leveraged_long=market.get("leveraged_long"),
                    leveraged_short=market.get("leveraged_short"),
                    leveraged_spreading=market.get("leveraged_spreading"),
                    other_reportable_long=market.get("other_reportable_long"),
                    other_reportable_short=market.get("other_reportable_short"),
                    nonreportable_long=market.get("nonreportable_long"),
                    nonreportable_short=market.get("nonreportable_short"),
                    confidence=0.95,
                    metadata=raw,
                )
            )
        return records
