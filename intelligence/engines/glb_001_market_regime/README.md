# GLB-001 Market Regime Engine

## Purpose
Classify the current global market environment into regimes.

## Inputs (via NDIP)
- `market.price.snapshot` - Current prices, OHLCV
- `market.trend.snapshot` - Trend direction and strength
- `market.volatility.snapshot` - VIX, ATR, standard deviation
- `market.breadth.snapshot` - Advancers/decliners, new highs/lows
- `market.risk.snapshot` - Risk sentiment indicators
- `macro.conditions.snapshot` - GDP, CPI, Employment, PMI (from GLB-003)

## Outputs
1. Global Regime Report
   - Primary regime (RISK_ON, RISK_OFF, TRENDING, RANGING, TRANSITION, VOLATILE)
   - Secondary regime
   - Transition state
   - Regime score (0-100)
   - Confidence (0-100)
   - Market dimensions

2. Asset Context (Level 2)
   - Regime alignment per asset
   - Asset-specific regime score
   - Primary factor

## Architecture
Consumes NDIP contracts → Normalizes → Extracts state → Classifies regime → Builds evidence → Calculates confidence → Identifies risks → Generates report

## Testing
```bash
# Unit tests
pytest tests/unit/test_glb_001/

# Certification
python tests/certification/certify_glb_001.py

### File 13: `tests/unit/test_glb_001/test_classifier.py`

```bash
cat > tests/unit/test_glb_001/test_classifier.py << 'EOF'
import pytest
from intelligence.engines.glb_001_market_regime.constants import MarketRegime
from intelligence.engines.glb_001_market_regime.regime_classifier import RegimeClassifier
from intelligence.engines.glb_001_market_regime.schemas import MarketDimension


def test_risk_on_classification():
    classifier = RegimeClassifier()

    dimensions = {
        "risk_sentiment": MarketDimension(
            name="risk_sentiment",
            value=85,
            weight=0.25,
            contribution=21.25,
            direction="BULLISH"
        ),
        "volatility": MarketDimension(
            name="volatility",
            value=15,
            weight=0.15,
            contribution=2.25,
            direction="BULLISH"
        ),
        "macro_growth": MarketDimension(
            name="macro_growth",
            value=75,
            weight=0.10,
            contribution=7.5,
            direction="BULLISH"
        ),
        "liquidity": MarketDimension(
            name="liquidity",
            value=80,
            weight=0.05,
            contribution=4.0,
            direction="BULLISH"
        )
    }

    regime, score, _ = classifier.classify(dimensions)
    assert regime == MarketRegime.RISK_ON
    assert score > 70


def test_risk_off_classification():
    classifier = RegimeClassifier()

    dimensions = {
        "risk_sentiment": MarketDimension(
            name="risk_sentiment",
            value=15,
            weight=0.25,
            contribution=3.75,
            direction="BEARISH"
        ),
        "volatility": MarketDimension(
            name="volatility",
            value=85,
            weight=0.15,
            contribution=12.75,
            direction="BEARISH"
        ),
        "macro_growth": MarketDimension(
            name="macro_growth",
            value=20,
            weight=0.10,
            contribution=2.0,
            direction="BEARISH"
        )
    }

    regime, score, _ = classifier.classify(dimensions)
    assert regime == MarketRegime.RISK_OFF
    assert score > 70
