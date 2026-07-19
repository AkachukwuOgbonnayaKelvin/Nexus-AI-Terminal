# MKT-001 - Market Price Engine

## Purpose
Institutional market data acquisition with multi-source hierarchy for trading decision support.

## Source Hierarchy
1. **Tier 1 - Primary Execution-Market Feed**: Pepperstone MT5
2. **Tier 2 - Independent Market Validation**: Composite API
3. **Tier 3 - Historical Research**: Yahoo Finance

## Architecture

## Data Flow

## NDIP Topics
- market.price.tick
- market.price.ohlcv
- market.price.snapshot
- market.price.instrument
- market.price.quality

## Dependencies
- MetaTrader5
- Python 3.11+
- DAR Runtime

## Testing
```bash
python -m pytest tests/
