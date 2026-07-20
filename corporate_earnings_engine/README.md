# ECO-002 - Corporate Earnings Engine

## Purpose
Acquire, normalize, validate, and publish corporate earnings data from official sources.

## Source Hierarchy
1. **Tier 1 - Primary Sources**: SEC EDGAR, Company IR, Regulatory Filings
2. **Tier 2 - Secondary Sources**: Financial Modeling Prep, Alpha Vantage, Finnhub

## Data Domains
- Earnings (EPS, Revenue)
- Financial Statements (Income Statement, Balance Sheet, Cash Flow)
- Earnings Estimates
- Company Guidance
- Regulatory Filings

## NDIP Topics
- corporate.earnings.raw
- corporate.earnings.normalized
- corporate.financial_statements
- corporate.estimates
- corporate.guidance
- corporate.filings

## Dependencies
- GLO-001: Market Regime Engine
- GLO-002: Macro Engine

## Testing
```bash
python -m pytest tests/
