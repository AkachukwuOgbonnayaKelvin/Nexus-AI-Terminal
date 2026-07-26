"""Universal COT Record DTO."""

from datetime import datetime

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
    dealer_long: int | None = None
    dealer_short: int | None = None
    dealer_spreading: int | None = None

    # Commercial positions
    commercial_long: int | None = None
    commercial_short: int | None = None
    commercial_spreading: int | None = None

    # Asset Manager positions
    asset_manager_long: int | None = None
    asset_manager_short: int | None = None
    asset_manager_spreading: int | None = None

    # Leveraged Fund positions
    leveraged_long: int | None = None
    leveraged_short: int | None = None
    leveraged_spreading: int | None = None

    # Other Reportables
    other_reportable_long: int | None = None
    other_reportable_short: int | None = None

    # Nonreportables
    nonreportable_long: int | None = None
    nonreportable_short: int | None = None

    # Changes (calculated later)
    change_open_interest: int | None = None
    change_dealer_long: int | None = None
    change_dealer_short: int | None = None
    change_asset_manager_long: int | None = None
    change_asset_manager_short: int | None = None
    change_leveraged_long: int | None = None
    change_leveraged_short: int | None = None

    confidence: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
