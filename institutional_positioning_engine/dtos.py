"""Universal COT Record DTO."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UniversalCOTRecord(BaseModel):
    report_id: str
    provider: str = "cftc"
    report_date: datetime
    market_code: str
    market_name: str
    asset_class: str
    currency: str
    exchange: str
    open_interest: int

    # Dealer positions
    dealer_long: Optional[int] = None
    dealer_short: Optional[int] = None
    dealer_spreading: Optional[int] = None

    # Commercial positions
    commercial_long: Optional[int] = None
    commercial_short: Optional[int] = None
    commercial_spreading: Optional[int] = None

    # Asset Manager positions
    asset_manager_long: Optional[int] = None
    asset_manager_short: Optional[int] = None
    asset_manager_spreading: Optional[int] = None

    # Leveraged Fund positions
    leveraged_long: Optional[int] = None
    leveraged_short: Optional[int] = None
    leveraged_spreading: Optional[int] = None

    # Other Reportables
    other_reportable_long: Optional[int] = None
    other_reportable_short: Optional[int] = None

    # Nonreportables
    nonreportable_long: Optional[int] = None
    nonreportable_short: Optional[int] = None

    # Changes (calculated later)
    change_open_interest: Optional[int] = None
    change_dealer_long: Optional[int] = None
    change_dealer_short: Optional[int] = None
    change_asset_manager_long: Optional[int] = None
    change_asset_manager_short: Optional[int] = None
    change_leveraged_long: Optional[int] = None
    change_leveraged_short: Optional[int] = None

    confidence: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
