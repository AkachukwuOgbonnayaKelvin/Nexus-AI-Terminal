#!/usr/bin/env python3
"""
Re-export OHLC Data with Proper Structure
"""

import json
import os
import pickle
import sys
import types

print("=" * 70)
print("RE-EXPORTING OHLC DATA")
print("=" * 70)

# Create dummy classes for pickle loading
sys.modules["providers"] = types.ModuleType("providers")
sys.modules["providers.base"] = types.ModuleType("providers.base")


class OHLCVData:
    def __init__(self, *args, **kwargs):
        self.open = kwargs.get("open", [])
        self.high = kwargs.get("high", [])
        self.low = kwargs.get("low", [])
        self.close = kwargs.get("close", [])
        self.time = kwargs.get("time", [])
        self.volume = kwargs.get("volume", [])
        self.symbol = kwargs.get("symbol", "")
        self.timeframe = kwargs.get("timeframe", "")


sys.modules["providers.base"].OHLCVData = OHLCVData

# Load each symbol
data_dir = "market_price_engine/data"
symbols = []
export_data = {}

# Get all D1 files
for file in os.listdir(data_dir):
    if file.endswith("_D1.pkl"):
        symbol = file.replace("_D1.pkl", "")
        symbol = symbol.replace("^", "")
        symbols.append(symbol)

print(f"\nFound {len(symbols)} symbols")

for symbol in symbols[:10]:  # Start with first 10
    pkl_file = f"{data_dir}/{symbol}_D1.pkl"
    if os.path.exists(pkl_file):
        try:
            with open(pkl_file, "rb") as f:
                data = pickle.load(f)

            print(f"\nProcessing: {symbol}")

            if isinstance(data, list):
                # Data is a list - try to extract OHLC
                if len(data) > 0:
                    # Check if it's a list of OHLC objects
                    if hasattr(data[0], "close"):
                        close = [d.close for d in data]
                        open_p = [d.open for d in data]
                        high = [d.high for d in data]
                        low = [d.low for d in data]
                        time = [getattr(d, "time", i) for i, d in enumerate(data)]
                    else:
                        # Try to extract from attributes
                        close = []
                        open_p = []
                        high = []
                        low = []
                        time = []
                        for item in data:
                            if isinstance(item, dict):
                                close.append(item.get("close", 0))
                                open_p.append(item.get("open", 0))
                                high.append(item.get("high", 0))
                                low.append(item.get("low", 0))
                                time.append(item.get("time", ""))
                            elif hasattr(item, "close"):
                                close.append(item.close)
                                open_p.append(item.open)
                                high.append(item.high)
                                low.append(item.low)
                                time.append(getattr(item, "time", ""))

                    export_data[symbol] = {
                        "symbol": symbol,
                        "timeframe": "D1",
                        "close": close,
                        "open": open_p,
                        "high": high,
                        "low": low,
                        "time": time,
                        "count": len(close),
                    }
                    print(f"  Exported {len(close)} records")
            else:
                print(f"  Unknown type: {type(data)}")

        except Exception as e:
            print(f"  Error: {e}")

print(f"\nExported {len(export_data)} symbols")

# Save to file
with open("ohlc_data_export.json", "w") as f:
    json.dump(export_data, f, default=str)

print("\nSaved to ohlc_data_export.json")
