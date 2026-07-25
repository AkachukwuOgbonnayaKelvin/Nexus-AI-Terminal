#!/usr/bin/env python3
"""
Check PKL Data Structure
"""

import os
import pickle

import pandas as pd

print("=" * 70)
print("CHECKING PKL DATA STRUCTURE")
print("=" * 70)

# Load a sample pickle file
pkl_file = "market_price_engine/data/EURUSD_D1.pkl"

if os.path.exists(pkl_file):
    print(f"\nLoading: {pkl_file}")

    with open(pkl_file, "rb") as f:
        data = pickle.load(f)

    print(f"\nData type: {type(data)}")

    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())}")
        for key, value in data.items():
            print(f"  {key}: {type(value)}")
            if isinstance(value, (list, tuple)) and len(value) > 0:
                print(f"    First item: {value[0]}")
                print(f"    Length: {len(value)}")
    elif isinstance(data, list):
        print(f"Length: {len(data)}")
        if len(data) > 0:
            print(f"First item: {data[0]}")
            print(f"Last item: {data[-1]}")
    elif isinstance(data, pd.DataFrame):
        print(f"Shape: {data.shape}")
        print(f"Columns: {data.columns.tolist()}")
        print("Head:")
        print(data.head())
    else:
        print(f"Content: {data}")
else:
    print(f"File not found: {pkl_file}")

print("\n" + "=" * 70)
