"""
Phase 6: Distribution API - Output Assembler

Assembles all Phase 4 and Phase 5 outputs into a single
ConfluenceIntelligencePackage.
"""

import logging
from datetime import datetime
from typing import Any

from ..contracts import (
    AssetClassRating,
    GlobalEntityRating,
    GlobalRisk,
    GlobalTheme,
    HarmonizedResult,
)
from .package import ConfluenceIntelligencePackage

logger = logging.getLogger(__name__)


class OutputAssembler:
    """
    Assembles all completed intelligence into a single package.

    This is the first step in the Distribution API pipeline.
    """

    def assemble(
        self,
        entity_ratings: list[GlobalEntityRating],
        asset_class_ratings: list[AssetClassRating],
        harmonized_results: list[HarmonizedResult],
        global_regime: str = "UNKNOWN",
        global_regime_confidence: float = 0.0,
        global_risk_level: str = "UNKNOWN",
        global_risk_score: float = 0.0,
        key_drivers: list[str] | None = None,
        global_risks: list[GlobalRisk] | None = None,
        global_themes: list[GlobalTheme] | None = None,
        top_opportunities: list[dict[str, Any]] | None = None,
    ) -> ConfluenceIntelligencePackage:
        """
        Assemble all components into a ConfluenceIntelligencePackage.

        Args:
            entity_ratings: List of GlobalEntityRating from Phase 4
            asset_class_ratings: List of AssetClassRating from Phase 5
            harmonized_results: List of HarmonizedResult from Phase 3
            global_regime: Global regime classification
            global_regime_confidence: Confidence in regime
            global_risk_level: Global risk level
            global_risk_score: Global risk score
            key_drivers: List of key drivers
            global_risks: List of global risks
            global_themes: List of global themes
            top_opportunities: List of top opportunities

        Returns:
            ConfluenceIntelligencePackage: Complete package
        """
        logger.info("Assembling Confluence Intelligence Package...")
        logger.info(f"  Entity ratings: {len(entity_ratings)}")
        logger.info(f"  Asset-class ratings: {len(asset_class_ratings)}")
        logger.info(f"  Harmonized results: {len(harmonized_results)}")

        # If no drivers provided, extract from entity ratings
        if key_drivers is None:
            key_drivers = self._extract_drivers(entity_ratings)

        # If no global risks provided, extract from entity ratings
        if global_risks is None:
            global_risks = self._extract_global_risks(entity_ratings)

        # If no global themes provided, derive from data
        if global_themes is None:
            global_themes = self._derive_themes(
                entity_ratings, asset_class_ratings, global_regime
            )

        # If no top opportunities provided, derive from data
        if top_opportunities is None:
            top_opportunities = self._derive_opportunities(
                entity_ratings, asset_class_ratings
            )

        package = ConfluenceIntelligencePackage(
            entity_ratings=entity_ratings,
            asset_class_ratings=asset_class_ratings,
            harmonized_results=harmonized_results,
            global_regime=global_regime,
            global_regime_confidence=global_regime_confidence,
            global_risk_level=global_risk_level,
            global_risk_score=global_risk_score,
            key_drivers=key_drivers,
            global_risks=global_risks,
            global_themes=global_themes,
            top_opportunities=top_opportunities,
            timestamp=datetime.utcnow(),
        )

        logger.info(f"Package assembled: {package}")
        return package

    def _extract_drivers(self, entity_ratings: list[GlobalEntityRating]) -> list[str]:
        """Extract top drivers from entity ratings."""
        driver_map: dict[str, float] = {}

        for rating in entity_ratings:
            for driver in rating.drivers:
                if driver.name not in driver_map:
                    driver_map[driver.name] = 0.0
                driver_map[driver.name] += driver.strength

        # Sort by strength and return top 5
        sorted_drivers = sorted(driver_map.items(), key=lambda x: x[1], reverse=True)
        return [d[0] for d in sorted_drivers[:5]]

    def _extract_global_risks(
        self, entity_ratings: list[GlobalEntityRating]
    ) -> list[GlobalRisk]:
        """Extract global risks from entity ratings."""
        risk_map: dict[str, float] = {}

        for rating in entity_ratings:
            for risk in rating.risks:
                if risk.name not in risk_map:
                    risk_map[risk.name] = 0.0
                risk_map[risk.name] += risk.severity

        # Sort by severity and return top 5
        sorted_risks = sorted(risk_map.items(), key=lambda x: x[1], reverse=True)

        global_risks = []
        for name, severity in sorted_risks[:5]:
            global_risks.append(
                GlobalRisk(
                    name=name,
                    severity=severity,
                    description=f"Global risk from {name}",
                    affected_assets=[],
                )
            )

        return global_risks

    def _derive_themes(
        self,
        entity_ratings: list[GlobalEntityRating],
        asset_class_ratings: list[AssetClassRating],
        global_regime: str,
    ) -> list[GlobalTheme]:
        """Derive global themes from intelligence."""
        themes = []

        # Check if safe-haven theme exists
        safe_haven_currencies = ["USD", "JPY", "CHF"]
        safe_haven_scores = []
        for rating in entity_ratings:
            if rating.entity in safe_haven_currencies:
                safe_haven_scores.append(rating.score)

        if safe_haven_scores and sum(safe_haven_scores) / len(safe_haven_scores) > 50:
            themes.append(
                GlobalTheme(
                    name="SAFE_HAVEN_DEMAND",
                    strength=sum(safe_haven_scores) / len(safe_haven_scores),
                    description="Safe-haven currencies showing strength",
                )
            )

        # Check for equity weakness
        equity_ratings = [
            r for r in asset_class_ratings if r.asset_class.value == "EQUITIES"
        ]
        if equity_ratings and equity_ratings[0].score < -50:
            themes.append(
                GlobalTheme(
                    name="EQUITY_RISK_AVERSION",
                    strength=abs(equity_ratings[0].score),
                    description="Equities showing weakness",
                )
            )

        # Check for metals strength
        metals_ratings = [
            r for r in asset_class_ratings if r.asset_class.value in ["METALS", "GOLD"]
        ]
        if metals_ratings and metals_ratings[0].score > 70:
            themes.append(
                GlobalTheme(
                    name="METALS_STRENGTH",
                    strength=metals_ratings[0].score,
                    description="Metals showing strength",
                )
            )

        # Add regime-based theme
        if global_regime == "RISK_OFF":
            themes.append(
                GlobalTheme(
                    name="RISK_OFF_ENVIRONMENT",
                    strength=80.0,
                    description="Global risk-off environment",
                )
            )
        elif global_regime == "RISK_ON":
            themes.append(
                GlobalTheme(
                    name="RISK_ON_ENVIRONMENT",
                    strength=80.0,
                    description="Global risk-on environment",
                )
            )

        return themes

    def _derive_opportunities(
        self,
        entity_ratings: list[GlobalEntityRating],
        asset_class_ratings: list[AssetClassRating],
    ) -> list[dict[str, Any]]:
        """Derive top opportunities from intelligence."""
        opportunities = []

        # Find strongest entities
        sorted_entities = sorted(entity_ratings, key=lambda r: r.score, reverse=True)

        for entity in sorted_entities[:3]:
            if entity.score > 50:
                opportunities.append(
                    {
                        "entity": entity.entity,
                        "type": entity.entity_type.value,
                        "score": entity.score,
                        "direction": entity.direction.value,
                        "confidence": entity.confidence,
                        "rationale": f"Strong {entity.entity_type.value} intelligence",
                    }
                )

        # Find strongest asset classes
        sorted_classes = sorted(
            asset_class_ratings, key=lambda r: r.score, reverse=True
        )

        for asset_class in sorted_classes[:2]:
            if asset_class.score > 50:
                opportunities.append(
                    {
                        "asset_class": asset_class.asset_class.value,
                        "name": asset_class.name,
                        "score": asset_class.score,
                        "direction": asset_class.direction.value,
                        "confidence": asset_class.confidence,
                        "rationale": f"Strong {asset_class.name} asset class",
                    }
                )

        return opportunities
