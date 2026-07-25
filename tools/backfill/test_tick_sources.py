"""
Test tick sources – MT5 or Mock.
"""

from datetime import datetime, timedelta

from intelligence.data.tick.sources import MockTickSource, MT5Source


def test_source(source):
    print(f"\n=== Testing {source.source_id} ===")
    print("Capability:", source.capability)
    print("Health check:", source.health_check())

    # Fetch last 5 minutes
    end = datetime.utcnow()
    start = end - timedelta(minutes=5)
    from intelligence.data.tick.contracts import TickRequest

    request = TickRequest(
        symbol="EURUSD",
        start=start,
        end=end,
        max_ticks=1000,
    )
    response = source.fetch(request)
    print("Fetch success:", response.success)
    print("Ticks fetched:", response.tick_count)
    if response.tick_count > 0:
        print("First tick:", response.ticks[0])
    print("Latency:", response.latency_ms, "ms")
    if response.error:
        print("Error:", response.error)


def main():
    # Try MT5 first
    mt5 = MT5Source()
    if mt5.health_check():
        test_source(mt5)
    else:
        print("MT5 not available, using mock source.")
        mock = MockTickSource()
        test_source(mock)


if __name__ == "__main__":
    main()
