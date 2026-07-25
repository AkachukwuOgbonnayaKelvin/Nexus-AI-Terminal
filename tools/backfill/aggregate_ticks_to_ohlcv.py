import sqlite3
import time
from datetime import datetime


def aggregate_symbol(symbol, timeframe_minutes):
    """Aggregate ticks for a symbol into OHLCV bars."""
    conn = sqlite3.connect("nexus_data.db")
    cursor = conn.cursor()

    # Get all ticks for the symbol, ordered by timestamp
    rows = cursor.execute(
        """
        SELECT timestamp, bid, ask, last, volume
        FROM fact_tick
        WHERE symbol = ?
        ORDER BY timestamp ASC
    """,
        (symbol,),
    ).fetchall()

    if not rows:
        print(f"No ticks for {symbol}")
        return

    bars = []
    current_bar = None
    current_start = None

    for ts_str, bid, ask, last, volume in rows:
        ts = datetime.fromisoformat(ts_str)
        # Round down to the timeframe interval
        interval_start = ts.replace(
            minute=(ts.minute // timeframe_minutes) * timeframe_minutes,
            second=0,
            microsecond=0,
        )

        # Get the effective price: last > bid > ask
        if last and last > 0:
            price = last
        elif bid and ask:
            price = (bid + ask) / 2
        elif bid:
            price = bid
        elif ask:
            price = ask
        else:
            continue  # skip if no usable price

        if current_bar is None or interval_start != current_start:
            # Start a new bar
            if current_bar is not None:
                bars.append(current_bar)
            current_start = interval_start
            current_bar = {
                "symbol": symbol,
                "timeframe": f"M{timeframe_minutes}",
                "timestamp": interval_start.isoformat(),
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "tick_count": 0,
                "up_ticks": 0,
                "down_ticks": 0,
                "zero_ticks": 0,
                "pressure": 0.0,
                "imbalance": 0.0,
                "avg_spread": 0.0,
                "max_spread": 0.0,
                "min_spread": 0.0,
                "source_id": "aggregator",
                "quality_score": 0.5,
            }

        # Update bar
        current_bar["high"] = max(current_bar["high"], price)
        current_bar["low"] = min(current_bar["low"], price)
        current_bar["close"] = price
        current_bar["tick_count"] += 1

        # Spread tracking (if available)
        if bid is not None and ask is not None:
            spread = ask - bid
            if current_bar["avg_spread"] == 0:
                current_bar["avg_spread"] = spread
            else:
                current_bar["avg_spread"] = (current_bar["avg_spread"] + spread) / 2
            current_bar["max_spread"] = max(current_bar["max_spread"], spread)
            if current_bar["min_spread"] == 0 or current_bar["min_spread"] > spread:
                current_bar["min_spread"] = spread

    # Add the last bar
    if current_bar is not None:
        bars.append(current_bar)

    # Insert bars into fact_tick_aggregated
    inserted = 0
    for bar in bars:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO fact_tick_aggregated
                (symbol, timeframe, timestamp, open, high, low, close,
                 tick_count, up_ticks, down_ticks, zero_ticks,
                 pressure, imbalance, avg_spread, max_spread, min_spread,
                 source_id, quality_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    bar["symbol"],
                    bar["timeframe"],
                    bar["timestamp"],
                    bar["open"],
                    bar["high"],
                    bar["low"],
                    bar["close"],
                    bar["tick_count"],
                    0,
                    0,
                    0,
                    0.0,
                    0.0,
                    bar["avg_spread"],
                    bar["max_spread"],
                    bar["min_spread"],
                    bar["source_id"],
                    bar["quality_score"],
                    datetime.utcnow().isoformat(),
                ),
            )
            inserted += 1
        except Exception as e:
            print(f"Error inserting bar: {e}")

    conn.commit()
    conn.close()
    print(f"Inserted {inserted} bars for {symbol} M{timeframe_minutes}")


def aggregate_all():
    conn = sqlite3.connect("nexus_data.db")
    symbols = [
        row[0]
        for row in conn.execute("SELECT DISTINCT symbol FROM fact_tick ORDER BY symbol")
    ]
    conn.close()

    # List of timeframes to aggregate (in minutes)
    timeframes = [1, 5, 15, 60, 240, 1440]  # M1, M5, M15, H1, H4, D1

    for symbol in symbols:
        print(f"\nAggregating {symbol}...")
        for tf in timeframes:
            aggregate_symbol(symbol, tf)
            time.sleep(0.5)  # brief pause


if __name__ == "__main__":
    aggregate_all()
