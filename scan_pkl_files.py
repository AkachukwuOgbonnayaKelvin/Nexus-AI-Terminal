#!/usr/bin/env python3
"""
Scan All PKL Files
"""

import os
from collections import defaultdict

print("=" * 70)
print("SCANNING PKL FILES")
print("=" * 70)

data_dir = "market_price_engine/data"
symbols = defaultdict(list)
timeframes = set()

if os.path.exists(data_dir):
    print(f"\nDirectory: {data_dir}")
    print(f"Total files: {len(os.listdir(data_dir))}")

    for file in os.listdir(data_dir):
        if file.endswith(".pkl"):
            # Parse symbol and timeframe
            name = file.replace(".pkl", "")
            parts = name.split("_")

            if len(parts) >= 2:
                tf = parts[-1]
                symbol = "_".join(parts[:-1])
                # Clean special chars
                symbol = symbol.replace("^", "")
                symbols[symbol].append(tf)
                timeframes.add(tf)

    print(f"\nSymbols found: {len(symbols)}")
    print(f"Timeframes: {sorted(timeframes)}")

    # Group by symbol
    print("\nSample symbols:")
    for i, (symbol, tfs) in enumerate(list(symbols.items())[:20]):
        print(f"  {symbol}: {tfs}")

    # Count by category
    fx_count = sum(
        1
        for s in symbols
        if s
        in [
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "AUDUSD",
            "NZDUSD",
            "USDCAD",
            "USDCHF",
            "EURGBP",
            "EURJPY",
            "GBPJPY",
            "AUDJPY",
            "CADJPY",
            "CHFJPY",
            "NZDCAD",
            "NZ DJPY",
        ]
    )
    indices = sum(
        1
        for s in symbols
        if s
        in [
            "US500",
            "US100",
            "US30",
            "GER40",
            "UK100",
            "FRA40",
            "JP225",
            "HK50",
            "AU200",
        ]
    )
    commodities = sum(
        1
        for s in symbols
        if s in ["XAUUSD", "XAGUSD", "WTI", "BRENT", "Copper", "NGAS"]
    )

    print("\nCategories:")
    print(f"  FX: {fx_count}")
    print(f"  Indices: {indices}")
    print(f"  Commodities: {commodities}")

else:
    print(f"Directory not found: {data_dir}")

print("\n" + "=" * 70)
