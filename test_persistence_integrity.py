import sqlite3

DB_PATH = "nexus_sentiment.db"


def test_integrity(conn):
    c = conn.cursor()
    errors = []

    # 1. Record preservation
    c.execute("SELECT COUNT(*) FROM ndip_raw_sentiment")
    raw = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM ndip_normalized_sentiment")
    norm = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM ndip_sentiment_scores")
    scores = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM ndip_quality")
    qual = c.fetchone()[0]
    if not (raw == norm == scores == qual):
        errors.append(
            f"NDIP mismatch: raw={raw}, norm={norm}, scores={scores}, quality={qual}"
        )

    # 2. Warehouse projection matches NDIP
    c.execute("SELECT COUNT(*) FROM fact_sentiment")
    if c.fetchone()[0] != scores:
        errors.append("fact_sentiment count != ndip_sentiment_scores")
    c.execute("SELECT COUNT(*) FROM fact_quality")
    if c.fetchone()[0] != qual:
        errors.append("fact_quality count != ndip_quality")

    # 3. Orphan check
    c.execute("""
        SELECT COUNT(*) FROM fact_entity_sentiment fes
        LEFT JOIN dim_entity de ON fes.entity_id = de.id
        WHERE de.id IS NULL
    """)
    if c.fetchone()[0] > 0:
        errors.append("Orphan entity sentiment records found")

    # 4. Entity sentiment count matches NDIP entities
    c.execute("SELECT COUNT(*) FROM fact_entity_sentiment")
    fes = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM ndip_entities")
    if fes != c.fetchone()[0]:
        errors.append("fact_entity_sentiment count != ndip_entities count")

    if errors:
        print("❌ Integrity errors:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("✅ All integrity checks passed.")
        return True


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    success = test_integrity(conn)
    conn.close()
    exit(0 if success else 1)
