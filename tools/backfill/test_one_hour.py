from datetime import datetime, timedelta

from intelligence.data.tick.contracts import TickRequest
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter
from intelligence.data.tick.sources import MT5Source

symbol = "EURUSD"
source = MT5Source()
writer = TickSQLiteWriter()

end = datetime.utcnow()
start = end - timedelta(hours=1)

print(f"Fetching ticks for {symbol} from {start} to {end}")
request = TickRequest(symbol=symbol, start=start, end=end, max_ticks=100000)
response = source.fetch(request)

print(f"Success: {response.success}")
print(f"Ticks fetched: {response.tick_count}")

if response.tick_count > 0:
    # Convert to dicts for writer
    ticks_dict = []
    for t in response.ticks:
        ticks_dict.append(
            {
                "symbol": t.symbol,
                "timestamp": t.timestamp.isoformat(),
                "bid": t.bid,
                "ask": t.ask,
                "last": t.last,
                "volume": t.volume,
                "source_id": t.source_id,
                "quality_score": t.quality_score,
            }
        )

    # Write
    inserted = writer.write_fact_tick(ticks_dict)
    print(f"Inserted: {inserted}")

    # Verify count
    count = writer.get_count(symbol)
    print(f"Total in fact_tick for {symbol}: {count}")
