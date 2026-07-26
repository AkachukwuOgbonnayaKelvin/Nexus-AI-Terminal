"""
GLB-004 Economic Events Engine - Asset Impact Matrix
"""

from typing import Any

from intelligence.schemas.asset_impact import (
    AssetImpact,
    AssetImpactMatrix,
    AssetType,
    Direction,
    ImpactDriver,
    ImpactStatus,
)


class EventsAssetImpactMatrix:
    """Generate asset impacts from economic events"""

    SUPPORTED_ASSETS = [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "AUDUSD",
        "NZDUSD",
        "USDCAD",
        "USDCHF",
        "XAUUSD",
        "XAGUSD",
        "US500",
        "US100",
        "US30",
        "GER40",
        "UK100",
        "JP225",
    ]

    @classmethod
    def generate(
        cls, events: list[dict[str, Any]], confidence: float
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from events"""
        impacts = {}

        # Group events by currency
        events_by_currency = cls._group_events_by_currency(events)

        # Calculate impact for each asset
        for asset in cls.SUPPORTED_ASSETS:
            impact = cls._calculate_asset_impact(asset, events_by_currency, confidence)
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-004",
            engine_name="Economic Events Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "event_count": len(events),
                "high_impact_count": sum(
                    1 for e in events if e.get("impact") == "HIGH"
                ),
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _group_events_by_currency(cls, events: list[dict]) -> dict[str, list[dict]]:
        """Group events by currency"""
        grouped = {}
        for event in events:
            currency = event.get("currency", "USD")
            if currency not in grouped:
                grouped[currency] = []
            grouped[currency].append(event)
        return grouped

    @classmethod
    def _calculate_asset_impact(
        cls, asset: str, events_by_currency: dict, confidence: float
    ) -> AssetImpact:
        """Calculate impact for a single asset"""
        # Determine currency exposure
        if asset == "EURUSD":
            base, quote = "EUR", "USD"
        elif asset == "GBPUSD":
            base, quote = "GBP", "USD"
        elif asset == "USDJPY":
            base, quote = "USD", "JPY"
        elif asset in ["AUDUSD", "NZDUSD"]:
            base, quote = asset[:3], "USD"
        elif asset == "USDCAD":
            base, quote = "USD", "CAD"
        elif asset == "USDCHF":
            base, quote = "USD", "CHF"
        else:
            return cls._neutral_impact(asset, confidence)

        # Calculate scores from events
        base_score = cls._calculate_currency_score(base, events_by_currency, confidence)
        quote_score = cls._calculate_currency_score(
            quote, events_by_currency, confidence
        )

        score = base_score - quote_score

        # Limit to -100 to +100
        score = max(-100, min(100, score))

        direction = cls._get_direction(score)
        drivers = cls._get_drivers(base, quote, events_by_currency)

        return AssetImpact(
            asset=asset,
            asset_type=cls._get_asset_type(asset),
            score=score,
            direction=direction,
            confidence=confidence * 0.75,
            status=ImpactStatus.ANALYZED,
            drivers=[
                ImpactDriver(name=d, direction=direction, strength=0.7)
                for d in drivers[:3]
            ],
            relevance=0.70,
            engine_id="GLB-004",
            engine_name="Economic Events Engine",
        )

    @classmethod
    def _calculate_currency_score(
        cls, currency: str, events_by_currency: dict, confidence: float
    ) -> float:
        """Calculate score for a currency based on events"""
        events = events_by_currency.get(currency, [])
        if not events:
            return 50.0

        score = 50.0
        event_count = 0

        for event in events:
            impact = event.get("impact", "LOW")
            deviation = event.get("deviation", 0)
            event_type = event.get("event", "")

            # Calculate impact factor
            impact_factor = (
                1.0 if impact == "HIGH" else 0.5 if impact == "MEDIUM" else 0.2
            )

            # Deviation: positive or negative
            direction = 1 if deviation > 0 else -1 if deviation < 0 else 0

            # Event-specific adjustments
            if "CPI" in event_type:
                # High CPI = currency strength (rate expectations)
                score += direction * 5 * impact_factor
            elif "NFP" in event_type or "Employment" in event_type:
                # Strong employment = currency strength
                score += direction * 4 * impact_factor
            elif "GDP" in event_type:
                # Strong GDP = currency strength
                score += direction * 6 * impact_factor
            elif "Interest Rate" in event_type:
                # Rate hikes = currency strength
                score += direction * 8 * impact_factor
            else:
                score += direction * 3 * impact_factor

            event_count += 1

        # Normalize
        if event_count > 0:
            score = 50 + (score - 50) / event_count

        return max(0, min(100, score))

    @classmethod
    def _neutral_impact(cls, asset: str, confidence: float) -> AssetImpact:
        """Return neutral impact for unsupported assets"""
        return AssetImpact(
            asset=asset,
            asset_type=cls._get_asset_type(asset),
            score=0,
            direction=Direction.NEUTRAL,
            confidence=confidence * 0.2,
            status=ImpactStatus.NOT_COVERED,
            drivers=[],
            relevance=0.1,
            engine_id="GLB-004",
            engine_name="Economic Events Engine",
        )

    @classmethod
    def _get_direction(cls, score: float) -> Direction:
        if score > 10:
            return Direction.BULLISH
        elif score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL

    @classmethod
    def _get_drivers(cls, base: str, quote: str, events_by_currency: dict) -> list[str]:
        """Get drivers for the asset"""
        drivers = []
        base_events = events_by_currency.get(base, [])
        quote_events = events_by_currency.get(quote, [])

        if base_events:
            drivers.append(f"{base} events: {len(base_events)}")
        if quote_events:
            drivers.append(f"{quote} events: {len(quote_events)}")

        if not drivers:
            drivers.append("No significant events")

        return drivers

    @classmethod
    def _get_asset_type(cls, asset: str) -> AssetType:
        fx_pairs = [
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "AUDUSD",
            "NZDUSD",
            "USDCAD",
            "USDCHF",
        ]
        commodities = ["XAUUSD", "XAGUSD"]
        equities = ["US500", "US100", "US30", "GER40", "UK100", "JP225"]

        if asset in fx_pairs:
            return AssetType.FX
        elif asset in commodities:
            return AssetType.COMMODITY
        elif asset in equities:
            return AssetType.EQUITY
        return AssetType.FX
