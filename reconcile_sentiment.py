import sqlite3

db_path = "nexus_sentiment.db"


def check_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    return tables


def migrate(conn):
    cursor = conn.cursor()

    # 1. Create dim_entity if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_entity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT NOT NULL,
            entity_type TEXT,
            canonical_name TEXT,
            alias TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entity_name, entity_type)
        )
    """)

    # 2. Create fact_entity_sentiment if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_entity_sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id TEXT NOT NULL,
            entity_id INTEGER NOT NULL,
            sentiment_score REAL,
            confidence REAL,
            timestamp DATETIME,
            FOREIGN KEY (entity_id) REFERENCES dim_entity(id),
            UNIQUE(content_id, entity_id)
        )
    """)

    conn.commit()

    # 3. Check if ndip_entities exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='ndip_entities'"
    )
    if not cursor.fetchone():
        print("ERROR: ndip_entities table not found. Run backfill first.")
        return

    # 4. Get distinct entities from ndip_entities
    cursor.execute("""
        SELECT DISTINCT entity_name, entity_type
        FROM ndip_entities
        WHERE entity_name IS NOT NULL AND entity_name != ''
    """)
    entities = cursor.fetchall()
    print(f"Found {len(entities)} unique entity name/type combinations.")

    entity_cache = {}
    for name, etype in entities:
        # Insert into dim_entity if not exists
        cursor.execute(
            """
            INSERT OR IGNORE INTO dim_entity (entity_name, entity_type)
            VALUES (?, ?)
        """,
            (name, etype or "unknown"),
        )
        # Get the id
        cursor.execute(
            """
            SELECT id FROM dim_entity
            WHERE entity_name = ? AND entity_type = ?
        """,
            (name, etype or "unknown"),
        )
        row = cursor.fetchone()
        if row:
            entity_cache[name] = row[0]

    conn.commit()
    print(f"Inserted/updated {len(entity_cache)} entities into dim_entity.")

    # 5. Get content_id, entity_name, sentiment_score from ndip_entities + ndip_sentiment_scores
    cursor.execute("""
        SELECT DISTINCT
            ne.content_id,
            ne.entity_name,
            ss.sentiment_score,
            ss.confidence,
            ss.scored_at
        FROM ndip_entities ne
        LEFT JOIN ndip_sentiment_scores ss ON ne.content_id = ss.content_id
        WHERE ss.sentiment_score IS NOT NULL
    """)
    rows = cursor.fetchall()
    print(f"Found {len(rows)} content-entity-sentiment records to migrate.")

    inserted = 0
    for content_id, entity_name, score, conf, ts in rows:
        entity_id = entity_cache.get(entity_name)
        if not entity_id:
            # Try to find entity again (should not happen)
            cursor.execute(
                """
                SELECT id FROM dim_entity WHERE entity_name = ?
            """,
                (entity_name,),
            )
            row = cursor.fetchone()
            if row:
                entity_id = row[0]
            else:
                # Insert as unknown type
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO dim_entity (entity_name, entity_type)
                    VALUES (?, ?)
                """,
                    (entity_name, "unknown"),
                )
                cursor.execute(
                    """
                    SELECT id FROM dim_entity WHERE entity_name = ?
                """,
                    (entity_name,),
                )
                row = cursor.fetchone()
                entity_id = row[0] if row else None

        if entity_id:
            cursor.execute(
                """
                INSERT OR IGNORE INTO fact_entity_sentiment (
                    content_id,
                    entity_id,
                    sentiment_score,
                    confidence,
                    timestamp
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (content_id, entity_id, score, conf, ts),
            )
            inserted += 1

    conn.commit()
    print(f"Inserted {inserted} entity sentiment records into fact_entity_sentiment.")

    # 6. Final counts
    cursor.execute("SELECT COUNT(*) FROM dim_entity")
    dim_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM fact_entity_sentiment")
    fact_count = cursor.fetchone()[0]
    print("\nFINAL COUNTS:")
    print(f"  dim_entity: {dim_count}")
    print(f"  fact_entity_sentiment: {fact_count}")


if __name__ == "__main__":
    print("Connecting to database...")
    try:
        conn = sqlite3.connect(db_path)
        print("Connected.")
        migrate(conn)
        conn.close()
        print("\nReconciliation complete.")
    except Exception as e:
        print(f"Error: {e}")
