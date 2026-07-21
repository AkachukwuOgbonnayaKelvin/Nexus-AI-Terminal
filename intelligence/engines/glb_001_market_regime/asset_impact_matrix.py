"""
GLB-001 Asset Impact Matrix Generator - Canonical Contract

Translates market regime into asset impacts.
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


class RegimeAssetImpactMatrix:
    """Generate asset impacts from market regime - Canonical version"""

    # All FX pairs
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

    # Regime → Asset Impacts (-100 to +100)
    REGIME_IMPACTS = {
        "RISK_ON": {
            "XAUUSD": {
                "score": -35,
                "drivers": ["Risk on reduces safe haven"],
                "relevance": 0.80,
            },
            "US500": {
                "score": 88,
                "drivers": ["Risk appetite", "Growth"],
                "relevance": 0.90,
            },
            "US100": {
                "score": 92,
                "drivers": ["Risk appetite", "Tech"],
                "relevance": 0.90,
            },
            "BTCUSD": {
                "score": 85,
                "drivers": ["Risk on", "Liquidity"],
                "relevance": 0.70,
            },
            "ETHUSD": {"score": 88, "drivers": ["Risk on", "Tech"], "relevance": 0.65},
        },
        "RISK_OFF": {
            "XAUUSD": {
                "score": 82,
                "drivers": ["Safe haven demand"],
                "relevance": 0.80,
            },
            "USDJPY": {"score": 55, "drivers": ["Safe haven flows"], "relevance": 0.70},
            "USDCHF": {"score": 60, "drivers": ["Safe haven flows"], "relevance": 0.75},
            "US500": {"score": -78, "drivers": ["Risk aversion"], "relevance": 0.90},
            "US100": {
                "score": -82,
                "drivers": ["Risk aversion", "Tech selloff"],
                "relevance": 0.90,
            },
            "BTCUSD": {
                "score": -75,
                "drivers": ["Risk off", "Liquidity drain"],
                "relevance": 0.70,
            },
            "ETHUSD": {
                "score": -78,
                "drivers": ["Risk off", "Tech selloff"],
                "relevance": 0.65,
            },
            "AUDUSD": {"score": -75, "drivers": ["Risk aversion"], "relevance": 0.85},
            "NZDUSD": {"score": -72, "drivers": ["Risk aversion"], "relevance": 0.80},
            "US30": {"score": -75, "drivers": ["Risk aversion"], "relevance": 0.85},
            "US2Y": {
                "score": 50,
                "drivers": ["Risk off = yields down"],
                "relevance": 0.70,
            },
            "US10Y": {
                "score": 60,
                "drivers": ["Risk off = yields down"],
                "relevance": 0.75,
            },
            "US30Y": {
                "score": 55,
                "drivers": ["Risk off = yields down"],
                "relevance": 0.70,
            },
        },
    }

    @classmethod
    def generate(cls, primary_regime: str, confidence: float) -> AssetImpactMatrix:
        """Generate canonical asset impact matrix from regime"""
        impacts = {}
        regime_impacts = cls.REGIME_IMPACTS.get(primary_regime, {})

        all_assets = (
            cls.FX_PAIRS + cls.COMMODITIES + cls.EQUITIES + cls.BONDS + cls.CRYPTO
        )

        for asset in all_assets:
            if asset in regime_impacts:
                data = regime_impacts[asset]
                # Create driver objects
                drivers = [
                    ImpactDriver(
                        name=d,
                        direction=cls._get_direction_from_score(data["score"]),
                        strength=0.7,
                    )
                    for d in data["drivers"]
                ]
                impacts[asset] = AssetImpact(
                    asset=asset,
                    asset_type=cls._get_asset_type(asset),
                    score=data["score"],
                    direction=cls._get_direction_from_score(data["score"]),
                    confidence=confidence * 0.85,
                    status=ImpactStatus.ANALYZED,
                    drivers=drivers,
                    relevance=data.get("relevance", 0.5),
                    engine_id="GLB-001",
                    engine_name="Market Regime Engine",
                )
            else:
                # NOT_COVERED - engine doesn't have an opinion on this asset
                impacts[asset] = AssetImpact(
                    asset=asset,
                    asset_type=cls._get_asset_type(asset),
                    score=0,
                    direction=Direction.NEUTRAL,
                    confidence=confidence * 0.2,
                    status=ImpactStatus.NOT_COVERED,
                    drivers=[],
                    relevance=0.0,
                    engine_id="GLB-001",
                    engine_name="Market Regime Engine",
                )

        return AssetImpactMatrix(
            engine_id="GLB-001",
            engine_name="Market Regime Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "regime": primary_regime,
                "asset_count": len(impacts),
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _get_asset_type(cls, asset: str) -> AssetType:
        if asset in cls.FX_PAIRS:
            return AssetType.FX
        elif asset in cls.COMMODITIES:
            return AssetType.COMMODITY
        elif asset in cls.EQUITIES:
            return AssetType.EQUITY
        elif asset in cls.BONDS:
            return AssetType.BOND
        elif asset in cls.CRYPTO:
            return AssetType.CRYPTO
        return AssetType.FX

    @classmethod
    def _get_direction_from_score(cls, score: float) -> Direction:
        if score > 10:
            return Direction.BULLISH
        elif score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL
