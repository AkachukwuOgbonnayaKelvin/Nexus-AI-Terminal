#!/usr/bin/env python3
"""
Build Canonical Historical Memory from Raw Data
"""

import sys

sys.path.insert(0, ".")

import json
from pathlib import Path

from intelligence.memory.historical.builder import HistoricalMemoryBuilder

print("=" * 70)
print("BUILDING CANONICAL HISTORICAL MEMORY")
print("=" * 70)

# Load raw windows
raw_file = "historical_windows_glb009.json"
if not Path(raw_file).exists():
    print(f"\nRaw file not found: {raw_file}")
    sys.exit(1)

with open(raw_file, "r") as f:
    raw_windows = json.load(f)

print(f"\nLoaded {len(raw_windows)} raw windows")

# Build canonical windows
builder = HistoricalMemoryBuilder(min_coverage_ratio=0.50)
builder.load_raw_windows(raw_windows)
canonical_windows = builder.build_canonical_windows()

# Show stats
stats = builder.get_stats()
print("\nBuild Results:")
print(f"  Canonical Windows: {stats.get('total_canonical_windows', 0)}")
print(f"  Valid Windows: {stats.get('valid_windows', 0)}")
print(f"  Invalid Windows: {stats.get('invalid_windows', 0)}")
print(f"  Symbols: {stats.get('symbols_count', 0)}")

# Show asset coverage
asset_coverage = stats.get("asset_coverage", {})
if asset_coverage:
    print("\nAsset Coverage:")
    for symbol, coverage in sorted(
        asset_coverage.items(), key=lambda x: x[1], reverse=True
    )[:10]:
        print(f"  {symbol}: {coverage * 100:.1f}%")

# Save canonical windows
output_file = "canonical_historical_windows.json"
builder.save_canonical_windows(output_file)
print(f"\nSaved to {output_file}")

print("\n" + "=" * 70)
