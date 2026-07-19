"""Universal Position DTO – Stores all CFTC fields."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class UniversalPosition(BaseModel):
    """Universal position model for all CFTC data."""

    # Core Identity
    market_name: str
    market_code: Optional[str] = None
    report_date: datetime
    report_type: str = "unknown"

    # Market Classification
    asset_class: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None

    # Open Interest
    open_interest: Optional[int] = None
    total_traders: Optional[int] = None

    # Dealer/Intermediary
    dealer_long: Optional[int] = None
    dealer_short: Optional[int] = None
    dealer_spread: Optional[int] = None
    dealer_change_long: Optional[int] = None
    dealer_change_short: Optional[int] = None
    dealer_pct_oi: Optional[float] = None
    dealer_traders: Optional[int] = None

    # Asset Manager/Institutional
    asset_manager_long: Optional[int] = None
    asset_manager_short: Optional[int] = None
    asset_manager_spread: Optional[int] = None
    asset_manager_change_long: Optional[int] = None
    asset_manager_change_short: Optional[int] = None
    asset_manager_pct_oi: Optional[float] = None
    asset_manager_traders: Optional[int] = None

    # Leveraged Funds
    leveraged_long: Optional[int] = None
    leveraged_short: Optional[int] = None
    leveraged_spread: Optional[int] = None
    leveraged_change_long: Optional[int] = None
    leveraged_change_short: Optional[int] = None
    leveraged_pct_oi: Optional[float] = None
    leveraged_traders: Optional[int] = None

    # Producer/Merchant/Processor/User
    producer_long: Optional[int] = None
    producer_short: Optional[int] = None
    producer_spread: Optional[int] = None
    producer_change_long: Optional[int] = None
    producer_change_short: Optional[int] = None
    producer_pct_oi: Optional[float] = None
    producer_traders: Optional[int] = None

    # Swap Dealers
    swap_long: Optional[int] = None
    swap_short: Optional[int] = None
    swap_spread: Optional[int] = None
    swap_change_long: Optional[int] = None
    swap_change_short: Optional[int] = None
    swap_pct_oi: Optional[float] = None
    swap_traders: Optional[int] = None

    # Other Reportables
    other_reportable_long: Optional[int] = None
    other_reportable_short: Optional[int] = None
    other_reportable_change_long: Optional[int] = None
    other_reportable_change_short: Optional[int] = None
    other_reportable_pct_oi: Optional[float] = None
    other_reportable_traders: Optional[int] = None

    # Non-Reportables
    nonreportable_long: Optional[int] = None
    nonreportable_short: Optional[int] = None
    nonreportable_change_long: Optional[int] = None
    nonreportable_change_short: Optional[int] = None
    nonreportable_pct_oi: Optional[float] = None
    nonreportable_traders: Optional[int] = None

    # Concentration Ratios
    concentration_4_long: Optional[float] = None
    concentration_4_short: Optional[float] = None
    concentration_8_long: Optional[float] = None
    concentration_8_short: Optional[float] = None
    concentration_4_net: Optional[float] = None
    concentration_8_net: Optional[float] = None

    # Contract Information
    contract_size: Optional[str] = None
    crop_year: Optional[str] = None

    # Metadata
    source: str = "unknown"
    source_url: Optional[str] = None
    checksum: Optional[str] = None
    version: int = 1
    confidence: float = 1.0
    ingested_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude={"raw_data"})
