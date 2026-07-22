"""
GLB-005 Central Bank Intelligence Engine - Asset Impact Matrix Generator
"""

import logging
from typing import Dict, List, Any

from intelligence.schemas.asset_impact import (
    AssetImpact,
    AssetImpactMatrix,
    AssetType,
    Direction,
    ImpactStatus,
    ImpactDriver,
)
from ..constants import ASSET_CLASS_EXPOSURE

logger = logging.getLogger(__name__)


class AssetImpactMatrixGenerator:
    """Generate canonical asset impact matrix from central bank policy"""

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

    # Currency exposure to central banks
    CURRENCY_EXPOSURE = {
        "USD": {"FED": 1.0},
        "EUR": {"ECB": 1.0},
        "GBP": {"BOE": 1.0},
        "JPY": {"BOJ": 1.0},
        "CHF": {"SNB": 1.0},
        "CAD": {"BOC": 1.0},
        "AUD": {"RBA": 1.0},
        "NZD": {"RBNZ": 1.0},
    }

    @classmethod
    def generate(
        cls,
        banks: List[Any],
        divergence: Dict,
        rate_environment: Dict,
        confidence: float,
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from central bank policy"""
        impacts = {}

        # Build policy profiles
        policy_profiles = cls._build_policy_profiles(banks)

        for asset in cls.SUPPORTED_ASSETS:
            impact = cls._calculate_asset_impact(
                asset, policy_profiles, divergence, rate_environment, confidence
            )
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-005",
            engine_name="Central Bank Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={"bank_count": len(banks), "model_version": "1.0.0"},
        )

    @classmethod
    def _build_policy_profiles(cls, banks: List[Any]) -> Dict:
        """Build policy profiles from bank data"""
        profiles = {}
        for bank_data in banks:
            bank_name = bank_data.bank.value
            profiles[bank_name] = {
                "currency": bank_data.currency,
                "score": bank_data.policy_score,
                "rate": bank_data.current_rate,
                "stance": bank_data.policy_stance.value,
                "expected_12m": bank_data.rate_expectations.twelve_month,
                "confidence": bank_data.confidence,
            }
        return profiles

    @classmethod
    def _calculate_asset_impact(
        cls,
        asset: str,
        profiles: Dict,
        divergence: Dict,
        rate_env: Dict,
        confidence: float,
    ) -> AssetImpact:
        """Calculate impact for a single asset"""
        # Determine which currencies are in this asset
        currencies = cls._get_currencies_in_asset(asset)

        if len(currencies) == 2:
            # FX pair - compare two currencies
            base, quote = currencies[0], currencies[1]
            impact = cls._calculate_fx_impact(
                asset, base, quote, profiles, divergence, confidence
            )
        else:
            # Non-FX asset
            impact = cls._calculate_other_impact(
                asset, currencies, profiles, rate_env, confidence
            )

        return impact

    @classmethod
    def _calculate_fx_impact(
        cls,
        asset: str,
        base: str,
        quote: str,
        profiles: Dict,
        divergence: Dict,
        confidence: float,
    ) -> AssetImpact:
        """Calculate FX pair impact from policy divergence"""
        base_bank = cls._get_currency_bank(base)
        quote_bank = cls._get_currency_bank(quote)

        if not base_bank or not quote_bank:
            return cls._neutral_impact(asset, confidence)

        base_profile = profiles.get(base_bank, {})
        quote_profile = profiles.get(quote_bank, {})

        if not base_profile or not quote_profile:
            return cls._neutral_impact(asset, confidence)

        # Calculate policy differential
        base_score = base_profile.get("score", 50)
        quote_score = quote_profile.get("score", 50)
        policy_diff = base_score - quote_score

        # Calculate rate differential
        base_rate = base_profile.get("rate", 0)
        quote_rate = quote_profile.get("rate", 0)
        rate_diff = base_rate - quote_rate

        # Combined score (-100 to +100)
        score = (policy_diff * 0.6) + (rate_diff * 10 * 0.4)
        score = max(-100, min(100, score))

        direction = cls._get_direction(score)

        # Build drivers
        drivers = []
        if abs(policy_diff) > 10:
            drivers.append(
                f"{base_bank} policy score: {base_score:.1f} vs {quote_bank}: {quote_score:.1f}"
            )
        if abs(rate_diff) > 0.25:
            drivers.append(f"Rate differential: {rate_diff:.2f}%")

        return AssetImpact(
            asset=asset,
            asset_type=AssetType.FX,
            score=score,
            direction=direction,
            confidence=confidence * 0.85,
            status=ImpactStatus.ANALYZED
            if abs(score) > 5
            else ImpactStatus.NOT_COVERED,
            drivers=[
                ImpactDriver(name=d, direction=direction, strength=0.7)
                for d in drivers[:3]
            ],
            relevance=0.85 if drivers else 0.3,
            engine_id="GLB-005",
            engine_name="Central Bank Intelligence Engine",
        )

    @classmethod
    def _calculate_other_impact(
        cls,
        asset: str,
        currencies: List[str],
        profiles: Dict,
        rate_env: Dict,
        confidence: float,
    ) -> AssetImpact:
        """Calculate impact for non-FX assets"""
        # Find the primary currency exposure
        primary_currency = currencies[0] if currencies else "USD"
        primary_bank = cls._get_currency_bank(primary_currency)

        if not primary_bank or primary_bank not in profiles:
            return cls._neutral_impact(asset, confidence)

        profile = profiles[primary_bank]
        score = (profile.get("score", 50) - 50) * 0.5

        # Adjust for asset class
        asset_type = cls._get_asset_type(asset)
        exposure_factor = ASSET_CLASS_EXPOSURE.get(asset_type.value, 0.4)
        score = score * exposure_factor

        # Limit
        score = max(-100, min(100, score))
        direction = cls._get_direction(score)

        drivers = [f"{primary_bank} policy: {profile.get('stance', 'NEUTRAL')}"]

        return AssetImpact(
            asset=asset,
            asset_type=asset_type,
            score=score,
            direction=direction,
            confidence=confidence * 0.7,
            status=ImpactStatus.ANALYZED
            if abs(score) > 5
            else ImpactStatus.NOT_COVERED,
            drivers=[
                ImpactDriver(name=d, direction=direction, strength=0.6)
                for d in drivers[:2]
            ],
            relevance=0.5,
            engine_id="GLB-005",
            engine_name="Central Bank Intelligence Engine",
        )

    @classmethod
    def _neutral_impact(cls, asset: str, confidence: float) -> AssetImpact:
        """Return neutral impact"""
        return AssetImpact(
            asset=asset,
            asset_type=cls._get_asset_type(asset),
            score=0,
            direction=Direction.NEUTRAL,
            confidence=confidence * 0.2,
            status=ImpactStatus.NOT_COVERED,
            drivers=[],
            relevance=0.1,
            engine_id="GLB-005",
            engine_name="Central Bank Intelligence Engine",
        )

    @classmethod
    def _get_currencies_in_asset(cls, asset: str) -> List[str]:
        """Get currencies in an asset"""
        currencies = []
        for currency in ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"]:
            if currency in asset:
                currencies.append(currency)
        if not currencies:
            currencies = ["USD"]
        return currencies

    @classmethod
    def _get_currency_bank(cls, currency: str) -> str:
        """Get central bank for a currency"""
        mapping = {
            "USD": "FED",
            "EUR": "ECB",
            "GBP": "BOE",
            "JPY": "BOJ",
            "CHF": "SNB",
            "CAD": "BOC",
            "AUD": "RBA",
            "NZD": "RBNZ",
        }
        return mapping.get(currency, "")

    @classmethod
    def _get_direction(cls, score: float) -> Direction:
        if score > 10:
            return Direction.BULLISH
        elif score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL

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
