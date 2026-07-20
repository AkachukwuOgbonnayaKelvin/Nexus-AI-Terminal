# MAC-001 - Macroeconomic Statistics Engine

## Purpose
Acquire, normalize, validate, version, and publish macroeconomic statistics from official sources.

## Source Hierarchy
1. **Tier 1 - Official National Sources**: BEA, BLS, Federal Reserve, ECB, Eurostat, ONS, etc.
2. **Tier 2 - International Official Sources**: IMF, World Bank, OECD
3. **Tier 3 - Commercial Aggregator**: Trading Economics

## Data Domains
- GDP (8 currencies, 36 years historical)
- Inflation (CPI, PCE, PPI)
- Labor (Unemployment, Payrolls, Wages)
- Central Bank (Policy Rates, Balance Sheet)
- Growth (PMI, Industrial Production, Retail Sales)
- Trade (Imports, Exports, Trade Balance)
- Fiscal (Government Debt, Budget Balance)
- Housing (Housing Starts, House Prices)

## Revision Tracking
- All data revisions preserved as vintages
- Each observation tracks revision number
- Historical data includes vintage dates
- Prevents look-ahead bias in backtesting

## NDIP Topics
- macro.statistics.raw
- macro.statistics.normalized
- macro.statistics.validated
- macro.statistics.revised
- macro.statistics.vintage
- macro.statistics.current
- macro.statistics.release

## Dependencies
- GLO-001: Market Regime Engine
- GLO-002: Macro Engine

## Testing
```bash
python -m pytest tests/

