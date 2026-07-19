# Institutional Positioning Engine (INS-001)

## Purpose
Tracks institutional positioning using COT (Commitment of Traders) data and other market indicators to identify "smart money" flows.

## Status
Development

## Architecture

### Core Components
- **acquisition/**: Data acquisition from various sources
- **collectors/**: Specialized data collectors
- **configuration/**: Engine configuration management
- **discovery/**: Discovery of data sources and instruments
- **downloader/**: Data downloading and caching
- **gateway/**: API gateway for external access
- **historical/**: Historical data management
- **market_registry/**: Market instrument registry
- **normalization/**: Data normalization and standardization
- **observability/**: Metrics and monitoring
- **parser/**: COT data parsing and extraction
- **providers/**: Data provider implementations
- **publication/**: NDIP publication
- **runtime/**: DAR runtime integration
- **tests/**: Test suite
- **validation/**: Data validation
- **warehouse/**: Data warehousing

### Data Flow
1. Acquisition → Collectors → Downloader
2. Downloader → Parser → Normalization
3. Normalization → Validation → Warehouse
4. Warehouse → Publication → NDIP

## Dependencies
- GLO-001: Market Regime Engine
- GLO-002: Macro Engine

## NDIP Topics
- institutional.cot.raw
- institutional.cot.cleaned
- institutional.positioning.analytics
- institutional.smart_money.signal

## Testing
```bash
python -m pytest institutional_positioning_engine/tests/

```bash
# Create README for ECONOMIC_EVENTS_ENGINE
cat > economic_events_engine/README.md << 'EOF'
# Economic Events Engine (ECO-001)

## Purpose
Collects and analyzes economic events and their market impact.

## Status
Development

## Features
- Economic calendar integration
- Impact scoring
- Surprise analysis
- Historical event tracking

## Dependencies
- GLO-001: Market Regime Engine
- GLO-002: Macro Engine

## NDIP Topics
- economic.events.raw
- economic.events.cleaned
- economic.events.analytics

## Testing
```bash
python -m pytest tests/

```bash
# Create README for FINANCIAL_NEWS_ENGINE
cat > financial_news_engine/README.md << 'EOF'
# Financial News Engine (NEWS-001)

## Purpose
Acquires, normalizes, and analyzes financial news data.

## Status
Development

## Features
- Multi-source news aggregation
- Sentiment analysis
- Entity extraction
- Relevance scoring

## Dependencies
- GLO-001: Market Regime Engine
- ECO-001: Economic Events Engine

## NDIP Topics
- news.raw
- news.cleaned
- news.analytics

## Testing
```bash
python -m pytest tests/

```bash
# Create README for MACROECONOMIC_EVENTS_ENGINE
cat > macroeconomic_events_engine/README.md << 'EOF'
# Macroeconomic Events Engine (MAC-002)

## Purpose
Collects and analyzes macroeconomic events and indicators.

## Status
Development

## Features
- GDP analysis
- CPI/PPI tracking
- Employment data
- PMI analysis
- Interest rate monitoring

## Dependencies
- GLO-001: Market Regime Engine
- GLO-002: Macro Engine
- ECO-001: Economic Events Engine

## NDIP Topics
- macro.data.raw
- macro.data.cleaned
- macro.analytics

## Testing
```bash
python -m pytest tests/

## Phase 10: Run ACP Validation

Now let's run ACP to validate all engines:

```bash
# Run full platform scan
python acp/acp.py scan

# Check repair plan - should now show no unregistered engines
python acp/acp.py repair-plan

# Validate each engine individually
python acp/acp.py engine INS-001
python acp/acp.py engine ECO-001
python acp/acp.py engine NEWS-001
python acp/acp.py engine MAC-002
python acp/acp.py engine CENTRAL_BANK_ENGINE

# Run final scan
python acp/acp.py scan
# Create README for ECONOMIC_EVENTS_ENGINE
cat > economic_events_engine/README.md << 'EOF'
# Economic Events Engine (ECO-001)

## Purpose
Collects and analyzes economic events and their market impact.

## Status
Development

## Features
- Economic calendar integration
- Impact scoring
- Surprise analysis
- Historical event tracking

## Dependencies
- GLO-001: Market Regime Engine
- GLO-002: Macro Engine

## NDIP Topics
- economic.events.raw
- economic.events.cleaned
- economic.events.analytics

## Testing
```bash
python -m pytest tests/
