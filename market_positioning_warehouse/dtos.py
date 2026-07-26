"""Universal Position DTO – Stores all CFTC fields."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class UniversalPosition(BaseModel):
    """Universal position model for all CFTC data."""

    # Core Identity
    market_name: str
    market_code: str | None = None
    report_date: datetime
    report_type: str = "unknown"

    # Market Classification
    asset_class: str | None = None
    exchange: str | None = None
    currency: str | None = None

    # Open Interest
    open_interest: int | None = None
    total_traders: int | None = None

    # Dealer/Intermediary
    dealer_long: int | None = None
    dealer_short: int | None = None
    dealer_spread: int | None = None
    dealer_change_long: int | None = None
    dealer_change_short: int | None = None
    dealer_pct_oi: float | None = None
    dealer_traders: int | None = None

    # Asset Manager/Institutional
    asset_manager_long: int | None = None
    asset_manager_short: int | None = None
    asset_manager_spread: int | None = None
    asset_manager_change_long: int | None = None
    asset_manager_change_short: int | None = None
    asset_manager_pct_oi: float | None = None
    asset_manager_traders: int | None = None

    # Leveraged Funds
    leveraged_long: int | None = None
    leveraged_short: int | None = None
    leveraged_spread: int | None = None
    leveraged_change_long: int | None = None
    leveraged_change_short: int | None = None
    leveraged_pct_oi: float | None = None
    leveraged_traders: int | None = None

    # Producer/Merchant/Processor/User
    producer_long: int | None = None
    producer_short: int | None = None
    producer_spread: int | None = None
    producer_change_long: int | None = None
    producer_change_short: int | None = None
    producer_pct_oi: float | None = None
    producer_traders: int | None = None

    # Swap Dealers
    swap_long: int | None = None
    swap_short: int | None = None
    swap_spread: int | None = None
    swap_change_long: int | None = None
    swap_change_short: int | None = None
    swap_pct_oi: float | None = None
    swap_traders: int | None = None

    # Other Reportables
    other_reportable_long: int | None = None
    other_reportable_short: int | None = None
    other_reportable_change_long: int | None = None
    other_reportable_change_short: int | None = None
    other_reportable_pct_oi: float | None = None
    other_reportable_traders: int | None = None

    # Non-Reportables
    nonreportable_long: int | None = None
    nonreportable_short: int | None = None
    nonreportable_change_long: int | None = None
    nonreportable_change_short: int | None = None
    nonreportable_pct_oi: float | None = None
    nonreportable_traders: int | None = None

    # Concentration Ratios
    concentration_4_long: float | None = None
    concentration_4_short: float | None = None
    concentration_8_long: float | None = None
    concentration_8_short: float | None = None
    concentration_4_net: float | None = None
    concentration_8_net: float | None = None

    # Contract Information
    contract_size: str | None = None
    crop_year: str | None = None

    # Metadata
    source: str = "unknown"
    source_url: str | None = None
    checksum: str | None = None
    version: int = 1
    confidence: float = 1.0
    ingested_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude={"raw_data"})
