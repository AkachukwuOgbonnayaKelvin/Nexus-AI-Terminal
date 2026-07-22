import sqlite3
import random
from datetime import datetime

DB_PATH = "nexus_sentiment.db"


def create_tables(conn):
    c = conn.cursor()
    # NDIP tables
    c.execute("""CREATE TABLE IF NOT EXISTS ndip_raw_sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT NOT NULL,
        content_id TEXT NOT NULL,
        symbol TEXT,
        content_type TEXT,
        raw_text TEXT,
        raw_payload TEXT,
        retrieved_at DATETIME NOT NULL,
        UNIQUE(source_id, content_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ndip_normalized_sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        normalized_text TEXT NOT NULL,
        language TEXT,
        normalization_version TEXT,
        created_at DATETIME NOT NULL,
        UNIQUE(content_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ndip_sentiment_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        sentiment_score REAL NOT NULL,
        sentiment_label TEXT NOT NULL,
        model_name TEXT,
        model_version TEXT,
        scored_at DATETIME NOT NULL,
        UNIQUE(content_id, model_name, model_version)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ndip_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        entity_type TEXT,
        confidence REAL,
        extraction_model TEXT,
        UNIQUE(content_id, entity_name, entity_type)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ndip_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        quality_score REAL NOT NULL,
        quality_level TEXT,
        assessed_at DATETIME NOT NULL,
        UNIQUE(content_id)
    )""")
    # Warehouse tables
    c.execute("""CREATE TABLE IF NOT EXISTS fact_sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        symbol TEXT,
        sentiment_score REAL,
        sentiment_label TEXT,
        confidence REAL,
        quality_score REAL,
        source_id TEXT,
        timestamp DATETIME,
        processed_at DATETIME,
        UNIQUE(content_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS fact_quality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        quality_score REAL,
        quality_level TEXT,
        source_reliability REAL,
        freshness REAL,
        assessed_at DATETIME,
        UNIQUE(content_id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS dim_entity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_name TEXT NOT NULL,
        entity_type TEXT,
        canonical_name TEXT,
        alias TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(entity_name, entity_type)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS fact_entity_sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        sentiment_score REAL,
        confidence REAL,
        timestamp DATETIME,
        FOREIGN KEY (entity_id) REFERENCES dim_entity(id),
        UNIQUE(content_id, entity_id)
    )""")
    conn.commit()
    print("[OK] All tables created/verified.")


def generate_sample_data(conn):
    c = conn.cursor()
    symbols = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"]
    content_types = ["NEWS_ARTICLE", "OFFICIAL_STATEMENT"]
    entities_pool = {
        "USD": ["Federal Reserve", "USD", "US Economy", "Inflation"],
        "EUR": ["ECB", "EUR", "Eurozone", "Germany"],
        "GBP": ["Bank of England", "GBP", "UK", "Brexit"],
        "JPY": ["BOJ", "JPY", "Japan", "Yen"],
        "CHF": ["SNB", "CHF", "Switzerland", "Franc"],
        "CAD": ["Bank of Canada", "CAD", "Canada", "Oil"],
        "AUD": ["RBA", "AUD", "Australia", "Commodities"],
        "NZD": ["RBNZ", "NZD", "New Zealand", "Dairy"],
    }
    inserted = 0
    now = datetime.now().isoformat()
    for sym in symbols:
        for ctype in content_types:
            for i in range(5):
                content_id = f"{sym}_{ctype}_{i}"
                # Check existence – idempotent
                c.execute(
                    "SELECT 1 FROM ndip_raw_sentiment WHERE content_id = ?",
                    (content_id,),
                )
                if c.fetchone():
                    continue  # skip existing
                text = f"Market update on {sym}: {random.choice(['bullish', 'bearish', 'neutral'])} sentiment."
                if ctype == "OFFICIAL_STATEMENT":
                    text = f"Official statement from {random.choice(entities_pool[sym])} regarding {sym}."
                # NDIP raw
                c.execute(
                    """
                    INSERT OR IGNORE INTO ndip_raw_sentiment (source_id, content_id, symbol, content_type, raw_text, raw_payload, retrieved_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (ctype.lower(), content_id, sym, ctype, text, "{}", now),
                )
                # NDIP normalized
                c.execute(
                    """
                    INSERT OR IGNORE INTO ndip_normalized_sentiment (content_id, normalized_text, language, normalization_version, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (content_id, text.lower(), "en", "v1", now),
                )
                # NDIP sentiment
                score = random.uniform(-0.8, 0.8)
                label = (
                    "BULLISH"
                    if score > 0.2
                    else "BEARISH"
                    if score < -0.2
                    else "NEUTRAL"
                )
                c.execute(
                    """
                    INSERT OR IGNORE INTO ndip_sentiment_scores (content_id, sentiment_score, sentiment_label, model_name, model_version, scored_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (content_id, score, label, "finbert", "v1", now),
                )
                # NDIP entities
                ents = random.sample(
                    entities_pool[sym], min(2, len(entities_pool[sym]))
                )
                for ent in ents:
                    c.execute(
                        """
                        INSERT OR IGNORE INTO ndip_entities (content_id, entity_name, entity_type, confidence, extraction_model)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            content_id,
                            ent,
                            "INSTITUTION",
                            random.uniform(0.7, 0.99),
                            "spacy",
                        ),
                    )
                # NDIP quality
                quality = random.uniform(0.7, 1.0)
                level = (
                    "HIGH" if quality > 0.8 else "MEDIUM" if quality > 0.5 else "LOW"
                )
                c.execute(
                    """
                    INSERT OR IGNORE INTO ndip_quality (content_id, quality_score, quality_level, assessed_at)
                    VALUES (?, ?, ?, ?)
                """,
                    (content_id, quality, level, now),
                )
                inserted += 1
    conn.commit()
    print(f"[OK] Inserted {inserted} new sample records (skipped existing).")


def reconcile(conn):
    c = conn.cursor()
    # 1. Entities dimension
    c.execute(
        """SELECT DISTINCT entity_name, entity_type FROM ndip_entities WHERE entity_name IS NOT NULL"""
    )
    entities = c.fetchall()
    print(f"[INFO] Found {len(entities)} unique entity name/type combinations.")
    entity_cache = {}
    for name, etype in entities:
        c.execute(
            """
            INSERT OR IGNORE INTO dim_entity (entity_name, entity_type)
            VALUES (?, ?)
        """,
            (name, etype or "unknown"),
        )
        c.execute(
            """
            SELECT id FROM dim_entity WHERE entity_name = ? AND entity_type = ?
        """,
            (name, etype or "unknown"),
        )
        row = c.fetchone()
        if row:
            entity_cache[name] = row[0]
    conn.commit()
    print(f"[OK] Inserted/updated {len(entity_cache)} entities into dim_entity.")

    # 2. Entity sentiment facts
    c.execute("""
        SELECT DISTINCT
            ne.content_id,
            ne.entity_name,
            ss.sentiment_score,
            ss.scored_at
        FROM ndip_entities ne
        LEFT JOIN ndip_sentiment_scores ss ON ne.content_id = ss.content_id
        WHERE ss.sentiment_score IS NOT NULL
    """)
    rows = c.fetchall()
    print(f"[INFO] Found {len(rows)} content-entity-sentiment records to migrate.")
    inserted = 0
    for content_id, entity_name, score, ts in rows:
        entity_id = entity_cache.get(entity_name)
        if not entity_id:
            c.execute("SELECT id FROM dim_entity WHERE entity_name = ?", (entity_name,))
            row = c.fetchone()
            entity_id = row[0] if row else None
        if entity_id:
            confidence = 0.85
            c.execute(
                """
                INSERT OR IGNORE INTO fact_entity_sentiment (
                    content_id, entity_id, sentiment_score, confidence, timestamp
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (content_id, entity_id, score, confidence, ts),
            )
            inserted += 1
    conn.commit()
    print(
        f"[OK] Inserted {inserted} entity sentiment records into fact_entity_sentiment."
    )


def project_warehouse(conn):
    """Populate fact_sentiment and fact_quality from NDIP (idempotent)."""
    c = conn.cursor()
    before = conn.total_changes

    # fact_sentiment
    c.execute("""
        INSERT OR IGNORE INTO fact_sentiment (
            content_id, symbol, sentiment_score, sentiment_label,
            confidence, quality_score, source_id, timestamp, processed_at
        )
        SELECT
            ss.content_id,
            rs.symbol,
            ss.sentiment_score,
            ss.sentiment_label,
            0.85 AS confidence,
            q.quality_score,
            rs.source_id,
            ss.scored_at,
            datetime('now')
        FROM ndip_sentiment_scores ss
        JOIN ndip_raw_sentiment rs ON ss.content_id = rs.content_id
        LEFT JOIN ndip_quality q ON ss.content_id = q.content_id
    """)
    inserted_sentiment = conn.total_changes - before

    # fact_quality
    before2 = conn.total_changes
    c.execute("""
        INSERT OR IGNORE INTO fact_quality (
            content_id, quality_score, quality_level,
            source_reliability, freshness, assessed_at
        )
        SELECT
            content_id,
            quality_score,
            quality_level,
            0.9 AS source_reliability,
            1.0 AS freshness,
            assessed_at
        FROM ndip_quality
    """)
    inserted_quality = conn.total_changes - before2
    conn.commit()
    print(f"[OK] fact_sentiment inserted: {inserted_sentiment}")
    print(f"[OK] fact_quality inserted: {inserted_quality}")


def verify_integrity(conn):
    """Run persistence integrity checks."""
    c = conn.cursor()
    errors = []

    # 1. Record preservation: raw = normalized = scores = quality
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
            f"NDIP record mismatch: raw={raw}, norm={norm}, scores={scores}, quality={qual}"
        )

    # 2. Warehouse projection: fact_sentiment matches ndip_sentiment_scores
    c.execute("SELECT COUNT(*) FROM fact_sentiment")
    fact_s = c.fetchone()[0]
    if fact_s != scores:
        errors.append(f"fact_sentiment ({fact_s}) != ndip_sentiment_scores ({scores})")

    # 3. fact_quality matches ndip_quality
    c.execute("SELECT COUNT(*) FROM fact_quality")
    fact_q = c.fetchone()[0]
    if fact_q != qual:
        errors.append(f"fact_quality ({fact_q}) != ndip_quality ({qual})")

    # 4. Entity integrity: every fact_entity_sentiment points to existing dim_entity
    c.execute("""
        SELECT COUNT(*) FROM fact_entity_sentiment fes
        LEFT JOIN dim_entity de ON fes.entity_id = de.id
        WHERE de.id IS NULL
    """)
    orphans = c.fetchone()[0]
    if orphans > 0:
        errors.append(f"Orphan entity sentiment records: {orphans}")

    # 5. Check that fact_entity_sentiment count matches entity records in NDIP
    c.execute("SELECT COUNT(*) FROM fact_entity_sentiment")
    fes = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM ndip_entities")
    ndip_ent = c.fetchone()[0]
    if fes != ndip_ent:
        errors.append(f"fact_entity_sentiment ({fes}) != ndip_entities ({ndip_ent})")

    if errors:
        print("\n❌ Integrity errors found:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("\n✅ All integrity checks passed.")
        return True


def print_counts(conn):
    c = conn.cursor()
    tables = [
        "ndip_raw_sentiment",
        "ndip_normalized_sentiment",
        "ndip_sentiment_scores",
        "ndip_entities",
        "ndip_quality",
        "fact_sentiment",
        "fact_quality",
        "dim_entity",
        "fact_entity_sentiment",
    ]
    print("\n[VERIFY] Final counts:")
    for t in tables:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  {t}: {c.fetchone()[0]}")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    generate_sample_data(conn)
    reconcile(conn)
    project_warehouse(conn)
    verify_integrity(conn)
    print_counts(conn)
    conn.close()
    print("\n[OK] Sentiment Engine persistence fully hardened.")
