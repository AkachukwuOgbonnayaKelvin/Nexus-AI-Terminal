#!/usr/bin/env python3
"""
Load PKL files with dummy classes
"""

import os
import pickle
import sys
import types

print("=" * 70)
print("LOADING PKL WITH DUMMY CLASSES")
print("=" * 70)

# ============================================
# Create dummy modules and classes
# ============================================
sys.modules["providers"] = types.ModuleType("providers")
sys.modules["providers.base"] = types.ModuleType("providers.base")


# Define OHLCVData class
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
        self.provider = kwargs.get("provider", "")


# Register it
sys.modules["providers.base"].OHLCVData = OHLCVData

# ============================================
# Test loading
# ============================================
data_dir = "market_price_engine/data"
symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "US500"]
loaded_data = {}

for symbol in symbols:
    pkl_file = f"{data_dir}/{symbol}_D1.pkl"
    if os.path.exists(pkl_file):
        try:
            with open(pkl_file, "rb") as f:
                data = pickle.load(f)

            loaded_data[symbol] = data
            print(f"✅ {symbol}: loaded")

            # Check what we got
            if isinstance(data, OHLCVData):
                print("   OHLCVData object")
                print(
                    f"   Attributes: {[a for a in dir(data) if not a.startswith('_')]}"
                )
                if hasattr(data, "close") and data.close:
                    print(f"   Close prices: {len(data.close)}")
                    print(f"   First 3 closes: {data.close[:3]}")
                    print(f"   Last 3 closes: {data.close[-3:]}")
            elif isinstance(data, dict):
                print(f"   Dict with keys: {list(data.keys())}")
            else:
                print(f"   Type: {type(data)}")

        except Exception as e:
            print(f"❌ {symbol}: {e}")
    else:
        print(f"⚠️ {symbol}: file not found")

print("\n" + "=" * 70)
print(f"Loaded {len(loaded_data)} symbols")
print(f"Symbols: {list(loaded_data.keys())}")
print("=" * 70)

# Save the data for later use
if loaded_data:
    import json

    # Convert to JSON-serializable format
    export_data = {}
    for symbol, data in loaded_data.items():
        if isinstance(data, OHLCVData):
            export_data[symbol] = {
                "close": data.close if data.close else [],
                "open": data.open if data.open else [],
                "high": data.high if data.high else [],
                "low": data.low if data.low else [],
                "time": data.time if data.time else [],
                "volume": data.volume if data.volume else [],
                "symbol": data.symbol,
                "timeframe": data.timeframe,
            }
        elif isinstance(data, dict):
            export_data[symbol] = data

    with open("ohlc_data_export.json", "w") as f:
        json.dump(export_data, f, default=str)
    print("\n✅ Saved to ohlc_data_export.json")
