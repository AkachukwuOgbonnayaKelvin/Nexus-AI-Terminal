import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from datetime import datetime, timedelta

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

# Coverage requirements in days
REQUIREMENTS = {
    'D1': 5 * 365,
    'H4': 3 * 365,
    'H1': 2 * 365,
    'M15': 1 * 365,
    'M5': 180,
}

def main():
    today = datetime.now().date()
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Get all symbols and timeframes with counts and min/max
    cur.execute("""
        SELECT symbol, timeframe, COUNT(*), MIN(time), MAX(time)
        FROM raw.market_ohlcv
        GROUP BY symbol, timeframe
        ORDER BY symbol, timeframe;
    """)
    rows = cur.fetchall()
    conn.close()

    print("=" * 90)
    print("MISSING COVERAGE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print(f"{'Symbol':<12} {'TF':<6} {'Status':<10} {'Missing Start':<18} {'Missing End':<18} {'Current Bars':<10}")
    print("-" * 90)

    for symbol, tf, count, min_t, max_t in rows:
        if tf not in REQUIREMENTS:
            continue
        required_days = REQUIREMENTS[tf]
        required_start = today - timedelta(days=required_days)

        if min_t is None or max_t is None:
            status = "NO DATA"
            missing_start = required_start
            missing_end = today
        else:
            min_date = min_t.date()
            max_date = max_t.date()

            # Check if coverage is complete
            if min_date <= required_start and max_date >= today:
                status = "COMPLETE"
                missing_start = None
                missing_end = None
            else:
                status = "PARTIAL"
                # Missing at start
                if min_date > required_start:
                    missing_start = required_start
                else:
                    missing_start = None
                # Missing at end
                if max_date < today:
                    missing_end = today
                else:
                    missing_end = None

        # Only print if not complete
        if status != "COMPLETE":
            start_str = missing_start.strftime("%Y-%m-%d") if missing_start else "---"
            end_str = missing_end.strftime("%Y-%m-%d") if missing_end else "---"
            print(f"{symbol:<12} {tf:<6} {status:<10} {start_str:<18} {end_str:<18} {count:<10}")

    print("=" * 90)

if __name__ == "__main__":
    main()
EOFcat > scripts/list_missing_coverage.py << 'EOF'
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from datetime import datetime, timedelta

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

# Coverage requirements in days
REQUIREMENTS = {
    'D1': 5 * 365,
    'H4': 3 * 365,
    'H1': 2 * 365,
    'M15': 1 * 365,
    'M5': 180,
}

def main():
    today = datetime.now().date()
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Get all symbols and timeframes with counts and min/max
    cur.execute("""
        SELECT symbol, timeframe, COUNT(*), MIN(time), MAX(time)
        FROM raw.market_ohlcv
        GROUP BY symbol, timeframe
        ORDER BY symbol, timeframe;
    """)
    rows = cur.fetchall()
    conn.close()

    print("=" * 90)
    print("MISSING COVERAGE REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print(f"{'Symbol':<12} {'TF':<6} {'Status':<10} {'Missing Start':<18} {'Missing End':<18} {'Current Bars':<10}")
    print("-" * 90)

    for symbol, tf, count, min_t, max_t in rows:
        if tf not in REQUIREMENTS:
            continue
        required_days = REQUIREMENTS[tf]
        required_start = today - timedelta(days=required_days)

        if min_t is None or max_t is None:
            status = "NO DATA"
            missing_start = required_start
            missing_end = today
        else:
            min_date = min_t.date()
            max_date = max_t.date()

            # Check if coverage is complete
            if min_date <= required_start and max_date >= today:
                status = "COMPLETE"
                missing_start = None
                missing_end = None
            else:
                status = "PARTIAL"
                # Missing at start
                if min_date > required_start:
                    missing_start = required_start
                else:
                    missing_start = None
                # Missing at end
                if max_date < today:
                    missing_end = today
                else:
                    missing_end = None

        # Only print if not complete
        if status != "COMPLETE":
            start_str = missing_start.strftime("%Y-%m-%d") if missing_start else "---"
            end_str = missing_end.strftime("%Y-%m-%d") if missing_end else "---"
            print(f"{symbol:<12} {tf:<6} {status:<10} {start_str:<18} {end_str:<18} {count:<10}")

    print("=" * 90)

if __name__ == "__main__":
    main()
