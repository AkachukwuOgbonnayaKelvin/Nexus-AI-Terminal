from datetime import datetime
from typing import Any, Dict

from economic_events_engine.dtos import UniversalEconomicEvent


class FredAdapter:
    """Converts raw FRED data to UniversalEconomicEvent with rich mapping."""

    # Full mapping of FRED series IDs to internal fields
    SERIES_MAPPING = {
        # GDP
        "GDP": {
            "title": "Gross Domestic Product",
            "category": "GDP",
            "short_title": "GDP",
            "importance": "High",
            "frequency": "Quarterly",
            "country": "US",
            "currency": "USD",
        },
        "GDPC1": {
            "title": "Real GDP",
            "category": "GDP",
            "short_title": "GDP (Real)",
            "importance": "High",
            "frequency": "Quarterly",
            "country": "US",
            "currency": "USD",
        },
        # Inflation
        "CPIAUCSL": {
            "title": "Consumer Price Index",
            "category": "Inflation",
            "short_title": "CPI",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "CPILFESL": {
            "title": "Core CPI (ex-food & energy)",
            "category": "Inflation",
            "short_title": "Core CPI",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "PPIACO": {
            "title": "Producer Price Index",
            "category": "Inflation",
            "short_title": "PPI",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "PCEPI": {
            "title": "Personal Consumption Expenditures Price Index",
            "category": "Inflation",
            "short_title": "PCE",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "PCEPILFE": {
            "title": "Core PCE",
            "category": "Inflation",
            "short_title": "Core PCE",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Employment
        "UNRATE": {
            "title": "Unemployment Rate",
            "category": "Employment",
            "short_title": "Unemployment",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "PAYEMS": {
            "title": "Nonfarm Payrolls",
            "category": "Employment",
            "short_title": "NFP",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "CES0500000003": {
            "title": "Average Hourly Earnings",
            "category": "Employment",
            "short_title": "Wages",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "U6RATE": {
            "title": "U-6 Unemployment Rate",
            "category": "Employment",
            "short_title": "U-6",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Retail Sales
        "RSXFS": {
            "title": "Retail Sales",
            "category": "Retail",
            "short_title": "Retail Sales",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Industrial Production
        "INDPRO": {
            "title": "Industrial Production Index",
            "category": "Industrial",
            "short_title": "Industrial Production",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # PMI (Manufacturing)
        "NAPM": {
            "title": "Manufacturing PMI",
            "category": "PMI",
            "short_title": "Manufacturing PMI",
            "importance": "High",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Interest Rates
        "FEDFUNDS": {
            "title": "Federal Funds Rate",
            "category": "Interest Rate",
            "short_title": "Fed Funds",
            "importance": "High",
            "frequency": "Daily",
            "country": "US",
            "currency": "USD",
        },
        "DGS10": {
            "title": "10-Year Treasury Yield",
            "category": "Interest Rate",
            "short_title": "10Y Treasury",
            "importance": "High",
            "frequency": "Daily",
            "country": "US",
            "currency": "USD",
        },
        "DGS2": {
            "title": "2-Year Treasury Yield",
            "category": "Interest Rate",
            "short_title": "2Y Treasury",
            "importance": "High",
            "frequency": "Daily",
            "country": "US",
            "currency": "USD",
        },
        # Consumer Confidence
        "UMCSENT": {
            "title": "Consumer Sentiment",
            "category": "Consumer",
            "short_title": "Consumer Sentiment",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Housing
        "HOUST": {
            "title": "Housing Starts",
            "category": "Housing",
            "short_title": "Housing Starts",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "PERMIT": {
            "title": "Building Permits",
            "category": "Housing",
            "short_title": "Building Permits",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Money Supply
        "M2SL": {
            "title": "M2 Money Supply",
            "category": "Money Supply",
            "short_title": "M2",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Trade
        "BOPGSTB": {
            "title": "Trade Balance",
            "category": "Trade",
            "short_title": "Trade Balance",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        # Other
        "AWHMAN": {
            "title": "Average Weekly Hours (Manufacturing)",
            "category": "Employment",
            "short_title": "Weekly Hours",
            "importance": "Low",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "JTSJOL": {
            "title": "Job Openings",
            "category": "Employment",
            "short_title": "Job Openings",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
        "CSUSHPISA": {
            "title": "Case-Shiller Home Price Index",
            "category": "Housing",
            "short_title": "Home Prices",
            "importance": "Medium",
            "frequency": "Monthly",
            "country": "US",
            "currency": "USD",
        },
    }

    def adapt(self, raw: Dict[str, Any], provider_name: str) -> UniversalEconomicEvent:
        series_id = raw.get("series_id")
        meta = self.SERIES_MAPPING.get(
            series_id,
            {
                "title": series_id,
                "category": "Unknown",
                "short_title": series_id,
                "importance": "Medium",
                "frequency": "Monthly",
                "country": "US",
                "currency": "USD",
            },
        )
        # Determine release time: FRED provides date as string
        release_time = datetime.fromisoformat(raw["date"]) if raw.get("date") else datetime.now()
        return UniversalEconomicEvent(
            event_id=f"fred_{series_id}_{raw['date']}",
            provider=provider_name,
            provider_event_id=series_id,
            country=meta["country"],
            region="North America",
            currency=meta["currency"],
            title=meta["title"],
            short_title=meta["short_title"],
            category=meta["category"],
            subcategory=None,
            forecast=None,
            previous=None,
            actual=raw["value"],
            consensus=None,
            revised_previous=None,
            importance=meta["importance"],
            release_time_utc=release_time,
            release_time_local=None,
            timezone="America/New_York",
            frequency=meta["frequency"],
            status="Released",
            source_url=f"https://fred.stlouisfed.org/series/{series_id}",
            tags=[meta["category"]],
            affected_assets=["USD", "Treasuries", "Stocks"] if meta["importance"] == "High" else [],
            affected_markets=["FX", "Rates", "Equities"] if meta["importance"] == "High" else [],
            confidence=0.95,
            quality_score=0.95,
            metadata={"series_id": series_id},
        )
