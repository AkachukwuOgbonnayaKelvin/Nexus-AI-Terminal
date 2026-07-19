# Central Bank Engine

## Mission
Collect, process, and analyze central bank policy decisions, statements, and speeches.

## Architecture

## Data Sources
- Federal Reserve
- European Central Bank
- Bank of England
- Bank of Japan
- PBOC, SNB, RBA, RBNZ

## NDIP Topics
- central_bank.raw
- central_bank.cleaned
- central_bank.analytics

## Runtime
- Managed by DAR
- Schedule: Every minute
- Priority: 1 (Highest)

## Testing
```bash
python -m pytest tests/
