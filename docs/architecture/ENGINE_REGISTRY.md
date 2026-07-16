# ENGINE REGISTRY – Nexus AI Terminal

**Version**: 1.0
**Status**: Approved
**Scope**: All current and planned engines, grouped by domain, with IDs, providers, warehouses, consumers, maturity, dependencies, and data products.

---

## PROVIDER REGISTRY (Master)

| ID | Provider | Tier | Capabilities | Status |
|----|----------|------|--------------|--------|
| PROV-001 | MT5 | 1 | Price (Forex, CFDs) | Active |
| PROV-002 | Polygon | 1 | Price (Equities, ETFs, Indices) | Active |
| PROV-003 | DXFeed | 1 | Price (Futures, Options) | Planned |
| PROV-004 | TradingEconomics | 1 | Economic Calendar | Planned |
| PROV-005 | Econoday | 1 | Economic Calendar | Planned |
| PROV-006 | Bloomberg | 1 | Enterprise Feed | Future |
| PROV-007 | Refinitiv | 1 | Enterprise Feed | Future |
| PROV-008 | Yahoo Finance | 2 | Price, Metadata | Active |
| PROV-009 | Alpha Vantage | 2 | Price, Metadata | Active |
| PROV-010 | Twelve Data | 2 | Price, Metadata | Planned |
| PROV-011 | FRED | 2 | Macro Statistics | Active |
| PROV-012 | ECB | 2 | Macro Statistics | Active |
| PROV-013 | Federal Reserve | 2 | Macro Statistics | Active |
| PROV-014 | BLS | 2 | Macro Statistics | Active |
| PROV-015 | BEA | 2 | Macro Statistics | Active |
| PROV-016 | CFTC | 2 | COT | Active |
| PROV-017 | Forex Factory | 3 | Economic Calendar | Planned |
| PROV-018 | Investing.com | 3 | Economic Calendar | Planned |
| PROV-019 | Binance | 3 | Crypto Price | Active |
| PROV-020 | Coinbase | 3 | Crypto Price | Planned |
| PROV-021 | NewsAPI | 3 | News | Planned |
| PROV-022 | RSS Feeds | 3 | News | Planned |
| PROV-023 | Manual Feed | 3 | Any | Planned |

---

## ENGINE INDEX

| ID | Engine Name | Domain | Maturity | Dependencies | Data Products |
|----|-------------|--------|----------|--------------|---------------|
| **MKT-001** | Market Price Engine | Raw – Market | **Certified** | Metadata Engine | OHLC, Volatility, Volume |
| **REF-001** | Market Metadata Engine | Raw – Reference | **Certified** | None | Asset Registry, Exchange Registry, Currency Registry |
| **MAC-001** | Macroeconomic Statistics Engine | Raw – Macro | **Certified** | Metadata Engine, Currency Registry, Country Registry | GDP, CPI, PPI, PCE, Unemployment, Retail Sales, PMI, Interest Rates, etc. |
| **MAC-002** | Economic Calendar Engine | Raw – Macro | **Concept** | Macro Statistics Engine, Metadata Engine | Upcoming Events, Forecasts, Consensus |
| **INS-001** | COT Engine | Raw – Institutional | **Concept** | Metadata Engine | Dealer, Commercial, Managed Money positions |
| **NEWS-001** | News Engine | Raw – News | **Concept** | Metadata Engine, Sentiment Engine | News Articles, Headlines, Sentiment Scores |
| **SENT-001** | Sentiment Engine | Raw – Sentiment | **Concept** | News Engine | Retail, Institutional, Social Media Sentiment |
| **INT-001** | Intermarket Engine | Intelligence | **Concept** | Price Engine, Macro Stats Engine, Bond Engine | Correlations, Lead-lag, Spillover |
| **GLB-001** | Global Intelligence | Intelligence | **Concept** | All Macro, Price, News, Sentiment | Macro Overview, Risk-on/off, Asset Allocation |
| **TEC-001** | Technical Intelligence | Intelligence | **Concept** | Price Engine | Technical Indicators, Patterns, Support/Resistance |
| **INSI-001** | Institutional Intelligence | Intelligence | **Concept** | COT, ETF Flow, Options | Institutional Positioning, Flow Analysis |
| **AI-001** | Executive AI | Intelligence | **Concept** | All engines | Predictions, Summaries, Anomalies, Insights |
| **DASH-001** | General Dashboard | Presentation | **Concept** | All engines | Visualisations, Widgets, Alerts |
| **API-001** | API Gateway | Presentation | **Concept** | All engines | REST, GraphQL, WebSocket |

---

## ENGINE DETAILS (Abbreviated)

### MKT-001 – Market Price Engine
- **Certified** – providers: MT5, Polygon, Yahoo, Alpha Vantage, Binance – warehouses: price_* – consumers: Technical, Asset, Intermarket, Dashboard.

### REF-001 – Market Metadata Engine
- **Certified** – providers: Yahoo, MT5, Polygon – warehouses: asset_registry, exchange_registry, currency_registry, etc. – consumers: All engines.

### MAC-001 – Macroeconomic Statistics Engine
- **Certified** – providers: FRED, ECB, BLS, BEA, Federal Reserve – warehouse: macro_stats – consumers: Global Intelligence, Asset Intelligence, AI, Reports.

### MAC-002 – Economic Calendar Engine
- **Concept** – providers: TradingEconomics (T1), Econoday (T1), Forex Factory (T2), Investing.com (T2) – warehouse: economic_calendar – consumers: Global Intelligence, Sentiment, Dashboard.

... (full details will be expanded as engines are built)

---

## DATA PRODUCTS (Cross-cutting)

| Product | Description | Derived From | Consumers |
|---------|-------------|--------------|-----------|
| OHLC | Open, High, Low, Close for multiple timeframes | Price Engine | Technical Intelligence, Asset Intelligence |
| Volatility | Historical and implied volatility | Price Engine | Intermarket, Executive AI |
| Macro Snapshot | Latest GDP, CPI, PMI, etc. | Macro Statistics Engine | Global Intelligence, Dashboard |
| Calendar Alerts | Upcoming high‑impact events | Economic Calendar Engine | Dashboard, Executive AI |
| Sentiment Aggregates | Retail, institutional, social sentiment | Sentiment Engine | Global Intelligence, Executive AI |
