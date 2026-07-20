# ECO-002 Corporate Earnings Engine

## Architecture Overview

### Components
- **Providers**: SEC EDGAR (Tier 1), Financial Modeling Prep (Tier 2)
- **Collectors**: Earnings data collection
- **Parsers**: Earnings and financial statement parsing
- **Normalizers**: Currency and period normalization
- **Validators**: Schema and data quality validation
- **Warehouse**: Persistent storage
- **NDIP**: Data publication

### Data Flow

### Source Hierarchy
1. Tier 1: SEC EDGAR (Primary)
2. Tier 2: Financial Modeling Prep, Alpha Vantage, Finnhub

### NDIP Topics
- corporate.earnings.raw
- corporate.earnings.normalized
- corporate.financial_statements
- corporate.estimates
- corporate.guidance
- corporate.filings
