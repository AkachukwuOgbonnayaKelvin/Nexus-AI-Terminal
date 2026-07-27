import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict
from datetime import datetime, timedelta

import psycopg2

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

# Define coverage requirements (same as our policy)
REQUIREMENTS = {
    "D1": 5 * 365,  # days
    "H4": 3 * 365,
    "H1": 2 * 365,
    "M15": 1 * 365,
    "M5": 180,
}


def get_coverage():
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Get all symbol/timeframe combinations with count and min/max time
    cur.execute("""
        SELECT symbol, timeframe, COUNT(*), MIN(time), MAX(time)
        FROM raw.market_ohlcv
        GROUP BY symbol, timeframe
        ORDER BY symbol, timeframe;
    """)
    rows = cur.fetchall()
    conn.close()

    report = []
    today = datetime.now().date()

    for symbol, tf, count, min_t, max_t in rows:
        if tf not in REQUIREMENTS:
            continue
        required_days = REQUIREMENTS[tf]
        earliest_required = today - timedelta(days=required_days)

        # Determine status
        if min_t is None or max_t is None:
            status = "NO_DATA"
            missing_start = earliest_required
            missing_end = today
        else:
            # Check if coverage meets requirements
            min_date = min_t.date()
            max_date = max_t.date()
            (max_date - min_date).days

            if min_date <= earliest_required and max_date >= today:
                status = "COMPLETE"
                missing_start = None
                missing_end = None
            else:
                status = "PARTIAL"
                # Missing ranges
                missing_start = (
                    max(min_date, earliest_required)
                    if min_date > earliest_required
                    else earliest_required
                )
                missing_end = today if max_date < today else None

        report.append(
            {
                "symbol": symbol,
                "timeframe": tf,
                "count": count,
                "min_date": min_t,
                "max_date": max_t,
                "status": status,
                "missing_start": missing_start,
                "missing_end": missing_end,
            }
        )

    return report


def main():
    report = get_coverage()
    print("=" * 90)
    print("COVERAGE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)

    # Group by symbol
    by_symbol = defaultdict(list)
    for r in report:
        by_symbol[r["symbol"]].append(r)

    for symbol in sorted(by_symbol.keys()):
        print(f"\n{symbol}")
        print("-" * 50)
        for r in by_symbol[symbol]:
            status = r["status"]
            if status == "COMPLETE":
                print(
                    f"  {r['timeframe']:4}  {r['count']:6} bars  {r['min_date']} → {r['max_date']}  ✅ COMPLETE"
                )
            elif status == "PARTIAL":
                print(
                    f"  {r['timeframe']:4}  {r['count']:6} bars  {r['min_date']} → {r['max_date']}  ⚠️ PARTIAL (missing: {r['missing_start']} → {r['missing_end']})"
                )
            else:
                print(f"  {r['timeframe']:4}  {r['count']:6} bars  ❌ NO DATA")

    print("\n" + "=" * 90)


if __name__ == "__main__":
    main()
