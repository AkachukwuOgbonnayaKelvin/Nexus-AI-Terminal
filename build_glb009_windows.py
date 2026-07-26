#!/usr/bin/env python3
"""
Build Complete Historical Windows for GLB-009
"""

import json

print("=" * 70)
print("BUILDING GLB-009 HISTORICAL WINDOWS")
print("=" * 70)

# Load OHLC data
with open("ohlc_data_export.json", "r") as f:
    ohlc_data = json.load(f)

print(f"\nLoaded {len(ohlc_data)} symbols")

# Build windows for each symbol
all_windows = []
window_size = 30  # 30-day window
horizons = [1, 3, 5, 10]  # 1D, 3D, 5D, 10D

for symbol, ohlc in ohlc_data.items():
    close_prices = ohlc.get("close", [])
    time_data = ohlc.get("time", [])

    if len(close_prices) < window_size + max(horizons):
        print(f"Warning: {symbol} has insufficient data ({len(close_prices)} prices)")
        continue

    print(f"\nProcessing: {symbol} ({len(close_prices)} prices)")

    # Build windows
    window_count = 0
    for i in range(len(close_prices) - window_size - max(horizons) + 1):
        # Get window prices
        window_prices = close_prices[i : i + window_size]

        # Get window dates if available
        window_dates = []
        if time_data and i + window_size <= len(time_data):
            window_dates = time_data[i : i + window_size]

        # Calculate forward returns
        forward_returns = {}
        current_price = window_prices[-1]
        for h in horizons:
            idx = i + window_size + h - 1
            if idx < len(close_prices):
                future_price = close_prices[idx]
                forward_returns[f"{h}D"] = (
                    (future_price - current_price) / current_price * 100
                )

        window = {
            "symbol": symbol,
            "start_idx": i,
            "window_prices": window_prices,
            "window_dates": window_dates if window_dates else [],
            "current_price": current_price,
            "forward_returns": forward_returns,
            "window_count": len(window_prices),
        }
        all_windows.append(window)
        window_count += 1

    print(f"  Built {window_count} windows")

print(f"\nTotal windows built: {len(all_windows)}")
print(f"  Symbols: {len(set(w['symbol'] for w in all_windows))}")

# Group by symbol
symbol_counts = {}
for w in all_windows:
    symbol = w["symbol"]
    symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1

print("\nWindows per symbol:")
for symbol, count in sorted(symbol_counts.items())[:10]:
    print(f"  {symbol}: {count}")

# Save windows
with open("historical_windows_glb009.json", "w") as f:
    json.dump(all_windows, f, default=str)
print("\nSaved to historical_windows_glb009.json")

# Show sample
if all_windows:
    sample = all_windows[0]
    print("\nSample window:")
    print(f"  Symbol: {sample['symbol']}")
    print(f"  Prices: {sample['window_prices'][:5]}...")
    print(f"  Forward returns: {sample['forward_returns']}")
