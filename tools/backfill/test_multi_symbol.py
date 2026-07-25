from datetime import datetime, timedelta

from intelligence.data.tick.contracts import TickRequest
from intelligence.data.tick.sources import MT5Source

symbols = ["EURUSD", "USDJPY", "XAUUSD", "US100", "CL=F"]
source = MT5Source()

if not source.health_check():
    print("MT5 not available")
    exit()

end = datetime.utcnow()
start = end - timedelta(minutes=5)

for symbol in symbols:
    print(f"\n=== Testing {symbol} ===")
    request = TickRequest(symbol=symbol, start=start, end=end, max_ticks=1000)
    response = source.fetch(request)
    if response.success:
        print("  Success: True")
        print(f"  Ticks: {response.tick_count}")
        if response.tick_count > 0:
            tick = response.ticks[0]
            print(f"  First tick: {tick}")
            print(f"  Effective price: {tick.effective_price}")
            print(f"  Spread: {tick.spread}")
    else:
        print(f"  Error: {response.error}")
