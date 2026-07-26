"""
GLB-002 Asset Impact Matrix Generator - Canonical Contract

Converts currency strengths and pair differentials into canonical asset impacts.
Uses internal -100 to +100 scale.
"""

from intelligence.schemas.asset_impact import (
    AssetImpact,
    AssetImpactMatrix,
    AssetType,
    Direction,
    ImpactDriver,
    ImpactStatus,
)


class AssetImpactMatrixGenerator:
    """Generate canonical asset impacts from currency strengths and pair analyses"""

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
        cls, currency_strengths: dict, pair_analyses: dict, confidence: float
    ) -> AssetImpactMatrix:
        """Generate canonical asset impact matrix"""
        impacts = {}
        all_assets = (
            cls.FX_PAIRS + cls.COMMODITIES + cls.EQUITIES + cls.BONDS + cls.CRYPTO
        )

        for asset in all_assets:
            impact = cls._generate_impact(
                asset, currency_strengths, pair_analyses, confidence
            )
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-002",
            engine_name="Asset Impact Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "currency_count": len(currency_strengths),
                "pair_count": len(pair_analyses),
                "asset_count": len(impacts),
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _generate_impact(
        cls,
        asset: str,
        currency_strengths: dict,
        pair_analyses: dict,
        confidence: float,
    ) -> AssetImpact:
        """Generate impact for a single asset"""
        # FX pairs from pair analyses
        if asset in pair_analyses:
            analysis = pair_analyses[asset]
            score = analysis.differential * 2.0
            score = max(-100, min(100, score))
            return AssetImpact(
                asset=asset,
                asset_type=AssetType.FX,
                score=score,
                direction=cls._get_direction(score),
                confidence=analysis.confidence,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name=d["factor"],
                        direction=cls._get_direction(d["impact"]),
                        strength=0.7,
                    )
                    for d in analysis.drivers[:3]
                ],
                relevance=0.85,
                engine_id="GLB-002",
                engine_name="Asset Impact Engine",
            )

        # FX pairs not in pair_analyses (derive from strengths)
        if asset in cls.FX_PAIRS:
            base = asset[:3]
            quote = asset[3:]
            base_strength = currency_strengths.get(base, None)
            quote_strength = currency_strengths.get(quote, None)

            if base_strength and quote_strength:
                diff = base_strength.score - quote_strength.score
                score = diff * 2.0
                score = max(-100, min(100, score))
                return AssetImpact(
                    asset=asset,
                    asset_type=AssetType.FX,
                    score=score,
                    direction=cls._get_direction(score),
                    confidence=confidence * 0.6,
                    status=ImpactStatus.ANALYZED,
                    drivers=[
                        ImpactDriver(
                            name="Currency strength differential",
                            direction=cls._get_direction(score),
                            strength=0.5,
                        )
                    ],
                    relevance=0.60,
                    engine_id="GLB-002",
                    engine_name="Asset Impact Engine",
                )
            else:
                return cls._not_covered(asset, AssetType.FX, confidence)

        # Commodities - derived from USD strength
        if asset in cls.COMMODITIES:
            usd_strength = currency_strengths.get("USD", None)
            usd_score = usd_strength.score if usd_strength else 50
            risk_sentiment = currency_strengths.get("EUR", None)
            risk_score = (
                risk_sentiment.factors.get("risk_sentiment", 50)
                if risk_sentiment
                else 50
            )

            if asset == "XAUUSD":
                score = (50 - usd_score) * 1.2 + (50 - risk_score) * 0.3
                score = max(-100, min(100, score))
                drivers = ["USD strength", "Risk sentiment"]
            elif asset == "XAGUSD":
                score = (50 - usd_score) * 1.0 + (risk_score - 50) * 0.2
                score = max(-100, min(100, score))
                drivers = ["USD strength", "Industrial demand"]
            elif asset in ["WTI", "BRENT"]:
                score = (risk_score - 50) * 1.5 + (50 - usd_score) * 0.5
                score = max(-100, min(100, score))
                drivers = ["Risk sentiment", "Growth"]
            else:
                score = (risk_score - 50) * 1.0
                score = max(-100, min(100, score))
                drivers = ["Risk sentiment"]

            return AssetImpact(
                asset=asset,
                asset_type=AssetType.COMMODITY,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.6,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name=d, direction=cls._get_direction(score), strength=0.6
                    )
                    for d in drivers[:2]
                ],
                relevance=0.50,
                engine_id="GLB-002",
                engine_name="Asset Impact Engine",
            )

        # Equities - derived from risk sentiment
        if asset in cls.EQUITIES:
            risk_sentiment = currency_strengths.get("EUR", None)
            risk_score = (
                risk_sentiment.factors.get("risk_sentiment", 50)
                if risk_sentiment
                else 50
            )

            if asset in ["US100", "US500", "US30"]:
                multiplier = (
                    1.6 if asset == "US100" else 1.4 if asset == "US500" else 1.2
                )
                score = (risk_score - 50) * multiplier
                score = max(-100, min(100, score))
            else:
                score = (risk_score - 50) * 1.0
                score = max(-100, min(100, score))

            return AssetImpact(
                asset=asset,
                asset_type=AssetType.EQUITY,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.6,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name="Risk sentiment",
                        direction=cls._get_direction(score),
                        strength=0.6,
                    )
                ],
                relevance=0.40,
                engine_id="GLB-002",
                engine_name="Asset Impact Engine",
            )

        # Bonds - inverse of risk sentiment
        if asset in cls.BONDS:
            risk_sentiment = currency_strengths.get("EUR", None)
            risk_score = (
                risk_sentiment.factors.get("risk_sentiment", 50)
                if risk_sentiment
                else 50
            )
            score = (50 - risk_score) * 0.8
            score = max(-100, min(100, score))

            return AssetImpact(
                asset=asset,
                asset_type=AssetType.BOND,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.5,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name="Risk sentiment",
                        direction=cls._get_direction(score),
                        strength=0.5,
                    )
                ],
                relevance=0.30,
                engine_id="GLB-002",
                engine_name="Asset Impact Engine",
            )

        # Crypto - highly sensitive to risk sentiment
        if asset in cls.CRYPTO:
            risk_sentiment = currency_strengths.get("EUR", None)
            risk_score = (
                risk_sentiment.factors.get("risk_sentiment", 50)
                if risk_sentiment
                else 50
            )
            score = (risk_score - 50) * 2.0
            score = max(-100, min(100, score))

            return AssetImpact(
                asset=asset,
                asset_type=AssetType.CRYPTO,
                score=score,
                direction=cls._get_direction(score),
                confidence=confidence * 0.5,
                status=ImpactStatus.ANALYZED,
                drivers=[
                    ImpactDriver(
                        name="Risk sentiment",
                        direction=cls._get_direction(score),
                        strength=0.6,
                    )
                ],
                relevance=0.30,
                engine_id="GLB-002",
                engine_name="Asset Impact Engine",
            )

        return cls._not_covered(asset, AssetType.FX, confidence)

    @classmethod
    def _not_covered(
        cls, asset: str, asset_type: AssetType, confidence: float
    ) -> AssetImpact:
        """Create NOT_COVERED impact"""
        return AssetImpact(
            asset=asset,
            asset_type=asset_type,
            score=0,
            direction=Direction.NEUTRAL,
            confidence=confidence * 0.1,
            status=ImpactStatus.NOT_COVERED,
            drivers=[],
            relevance=0.0,
            engine_id="GLB-002",
            engine_name="Asset Impact Engine",
        )

    @classmethod
    def _get_direction(cls, score: float) -> Direction:
        if score > 10:
            return Direction.BULLISH
        elif score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL
