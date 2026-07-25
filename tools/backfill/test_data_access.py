from intelligence.technical import TechnicalDataAccess

td = TechnicalDataAccess()

print("Symbols:", td.get_symbols()[:10])
print("Timeframes:", td.get_timeframes())

# Test get_candles
df = td.get_candles("EURUSD", "D1", limit=5)
print("\nEURUSD D1 (last 5):")
print(df)

# Test coverage
cov = td.get_coverage("EURUSD", "D1")
print("\nEURUSD D1 coverage:", cov)

# Test multi-timeframe
multi = td.get_multi_timeframe("USDJPY", ["D1", "H1"], limit=3)
for tf, data in multi.items():
    print(f"\nUSDJPY {tf} (last 3):")
    print(data[["time", "close"]])
