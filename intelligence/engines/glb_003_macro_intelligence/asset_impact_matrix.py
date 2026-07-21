"""
GLB-003 Macro Intelligence Asset Impact Matrix Generator - Canonical Contract

Translates macroeconomic conditions into canonical asset impacts.
Uses internal -100 to +100 scale.
"""

from intelligence.schemas.asset_impact import (
    AssetImpact,
    AssetImpactMatrix,
    AssetType,
    Direction,
    ImpactStatus,
    ImpactDriver,
)


class MacroAssetImpactMatrix:
    """Generate canonical asset impacts from macroeconomic analysis"""

    FX_PAIRS = [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "AUDUSD",
        "NZDUSD",
        "USDCAD",
        "USDCHF",
        "EURGBP",
        "EURJPY",
        "EURAUD",
        "EURNZD",
        "EURCAD",
        "EURCHF",
        "GBPJPY",
        "GBPAUD",
        "GBPNZD",
        "GBPCAD",
        "GBPCHF",
        "AUDJPY",
        "AUDNZD",
        "AUDCAD",
        "AUDCHF",
        "NZDJPY",
        "NZDCAD",
        "NZDCHF",
        "CADJPY",
        "CHFJPY",
    ]

    COMMODITIES = [
        "XAUUSD",
        "XAGUSD",
        "XPTUSD",
        "XPDUSD",
        "WTI",
        "BRENT",
        "NGAS",
        "COPPER",
    ]
    EQUITIES = [
        "US500",
        "US100",
        "US30",
        "GER40",
        "UK100",
        "FRA40",
        "JP225",
        "HK50",
        "AU200",
        "CN50",
        "IN50",
        "BR60",
    ]
    BONDS = ["US2Y", "US10Y", "US30Y", "BUND", "GILT", "JGB"]
    CRYPTO = ["BTCUSD", "ETHUSD", "SOLUSD", "XRPUSD"]

    @classmethod
    def generate(
        cls,
        macro_score: float,
        growth_score: float,
        inflation_score: float,
        employment_score: float,
        confidence: float,
    ) -> AssetImpactMatrix:
        """Generate canonical asset impact matrix from macro analysis."""
        impacts = {}

        # Calculate macro sentiment (-100 to +100)
        macro_sentiment = (growth_score - 50) * 1.5
        macro_sentiment += (50 - inflation_score) * 0.5
        macro_sentiment += (employment_score - 50) * 0.5
        macro_sentiment = max(-100, min(100, macro_sentiment))

        all_assets = (
            cls.FX_PAIRS + cls.COMMODITIES + cls.EQUITIES + cls.BONDS + cls.CRYPTO
        )

        for asset in all_assets:
            impact = cls._generate_impact(asset, macro_sentiment, confidence)
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-003",
            engine_name="Macro Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "macro_score": macro_score,
                "growth_score": growth_score,
                "inflation_score": inflation_score,
                "employment_score": employment_score,
                "macro_sentiment": macro_sentiment,
                "asset_count": len(impacts),
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _generate_impact(
        cls, asset: str, sentiment: float, confidence: float
    ) -> AssetImpact:
        """Generate impact for a single asset"""
        # FX pairs
        if asset in cls.FX_PAIRS:
            if asset == "USDJPY":
                # JPY is safe haven
                score = -sentiment * 0.6
                drivers = ["Yield differential", "Risk sentiment"]
            elif asset in ["USDCAD", "USDCHF"]:
                score = -sentiment * 0.5
                drivers = ["Risk sentiment", "Growth"]
            else:
                # Pro-cyclical
                score = sentiment * 0.7
                drivers = ["Macro environment", "Growth differential"]
            score = max(-100, min(100, score))
            return AssetImpact(
                asset=asset,
                asset_type=AssetType.FX,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.75,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name=d, direction=cls._get_direction(score), strength=0.7
                    )
                    for d in drivers[:2]
                ],
                relevance=0.80,
                engine_id="GLB-003",
                engine_name="Macro Intelligence Engine",
            )

        # Commodities
        if asset in cls.COMMODITIES:
            if asset == "XAUUSD":
                # Gold: inverse real yields, inflation hedge
                score = -sentiment * 0.5
                drivers = ["Real yields", "Inflation hedge"]
            elif asset == "XAGUSD":
                # Silver: gold + industrial demand
                score = -sentiment * 0.35 + sentiment * 0.2
                drivers = ["Industrial demand", "Gold correlation"]
            elif asset in ["WTI", "BRENT"]:
                # Oil: positive growth
                score = sentiment * 0.7
                drivers = ["Global growth", "Demand"]
            else:
                # Other commodities
                score = sentiment * 0.5
                drivers = ["Macro conditions"]
            score = max(-100, min(100, score))
            return AssetImpact(
                asset=asset,
                asset_type=AssetType.COMMODITY,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.70,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name=d, direction=cls._get_direction(score), strength=0.6
                    )
                    for d in drivers[:2]
                ],
                relevance=0.60,
                engine_id="GLB-003",
                engine_name="Macro Intelligence Engine",
            )

        # Equities
        if asset in cls.EQUITIES:
            if asset in ["US100", "US500", "US30"]:
                multiplier = (
                    1.0 if asset == "US100" else 0.9 if asset == "US500" else 0.8
                )
                score = sentiment * multiplier
                drivers = (
                    ["Economic growth", "Earnings"]
                    if asset in ["US100", "US500"]
                    else ["Growth"]
                )
            else:
                score = sentiment * 0.7
                drivers = ["Global growth"]
            score = max(-100, min(100, score))
            return AssetImpact(
                asset=asset,
                asset_type=AssetType.EQUITY,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.80,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name=d, direction=cls._get_direction(score), strength=0.6
                    )
                    for d in drivers[:2]
                ],
                relevance=0.70,
                engine_id="GLB-003",
                engine_name="Macro Intelligence Engine",
            )

        # Bonds
        if asset in cls.BONDS:
            # Bonds: inverse of growth and inflation
            score = -sentiment * 0.3
            score = max(-100, min(100, score))
            return AssetImpact(
                asset=asset,
                asset_type=AssetType.BOND,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.65,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name="Growth expectations",
                        direction=cls._get_direction(score),
                        strength=0.5,
                    )
                ],
                relevance=0.50,
                engine_id="GLB-003",
                engine_name="Macro Intelligence Engine",
            )

        # Crypto
        if asset in cls.CRYPTO:
            score = sentiment * 1.0
            score = max(-100, min(100, score))
            return AssetImpact(
                asset=asset,
                asset_type=AssetType.CRYPTO,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.60,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name="Risk appetite",
                        direction=cls._get_direction(score),
                        strength=0.6,
                    )
                ],
                relevance=0.45,
                engine_id="GLB-003",
                engine_name="Macro Intelligence Engine",
            )

        # Should never reach here
        return AssetImpact(
            asset=asset,
            asset_type=AssetType.FX,
            score=0,
            direction=Direction.NEUTRAL,
            confidence=0.1,
            status=ImpactStatus.NOT_COVERED,
            drivers=[],
            relevance=0.0,
            engine_id="GLB-003",
            engine_name="Macro Intelligence Engine",
        )

    @classmethod
    def _get_direction(cls, score: float) -> Direction:
        if score > 10:
            return Direction.BULLISH
        elif score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL
