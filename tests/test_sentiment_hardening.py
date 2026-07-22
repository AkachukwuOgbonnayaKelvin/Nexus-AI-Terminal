"""
Comprehensive tests for the hardened Sentiment Engine.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine

from intelligence.data.sentiment.contracts.extracted_entity import (
    ExtractedEntity,
    EntitySentiment,
    EntityType,
    EntitySentimentLabel,
)
from intelligence.data.sentiment.persistence.entity_writer import (
    EntityWriter,
    EntityCanonicalizer,
)
from intelligence.data.sentiment.pipeline.sentiment_pipeline import SentimentPipeline
from intelligence.data.sentiment.feeds.sentiment_feed import SentimentFeed


class TestEntityCanonicalizer:
    """Test entity canonicalization."""

    def test_canonicalize_fed(self):
        assert EntityCanonicalizer.canonicalize("Fed") == "Federal Reserve"
        assert EntityCanonicalizer.canonicalize("federal reserve") == "Federal Reserve"
        assert EntityCanonicalizer.canonicalize("ECB") == "European Central Bank"

    def test_canonicalize_currency(self):
        assert EntityCanonicalizer.canonicalize("usd") == "USD"
        assert EntityCanonicalizer.canonicalize("EUR") == "EUR"

    def test_get_aliases(self):
        aliases = EntityCanonicalizer.get_aliases("Fed")
        assert "Fed" in aliases
        assert "Federal Reserve" in aliases


class TestEntityWriter:
    """Test entity persistence."""

    @pytest.fixture
    def db_engine(self):
        # Use an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        # Create tables (simplified)
        with engine.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dim_entity (
                    entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    canonical_name TEXT UNIQUE,
                    entity_type TEXT,
                    country TEXT,
                    currency TEXT,
                    aliases TEXT,
                    metadata TEXT,
                    created_at DATETIME,
                    updated_at DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_entity_sentiment (
                    fact_entity_sentiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentiment_id TEXT,
                    entity_id INTEGER,
                    entity_score REAL,
                    confidence REAL,
                    label TEXT,
                    timestamp DATETIME,
                    source_entities TEXT,
                    UNIQUE(sentiment_id, entity_id)
                )
            """)
            conn.commit()
        return engine

    def test_write_entity(self, db_engine):
        writer = EntityWriter(db_engine)
        entity = ExtractedEntity(
            canonical_name="Federal Reserve",
            original_name="Fed",
            entity_type=EntityType.INSTITUTION,
            country="US",
            currency="USD",
            aliases=["Fed", "Federal Reserve System"],
        )
        entities = writer.write_entities([entity])
        assert len(entities) == 1
        assert entities[0].entity_id is not None

        # Write again, should reuse
        entity2 = ExtractedEntity(
            canonical_name="Federal Reserve",
            original_name="The Fed",
            entity_type=EntityType.INSTITUTION,
            country="US",
            currency="USD",
            aliases=["The Fed"],
        )
        entities2 = writer.write_entities([entity2])
        assert len(entities2) == 1
        assert entities2[0].entity_id == entities[0].entity_id
        assert writer.stats["entities_reused"] == 1

    def test_write_entity_sentiment(self, db_engine):
        writer = EntityWriter(db_engine)
        # First write an entity
        entity = ExtractedEntity(
            canonical_name="Federal Reserve",
            original_name="Fed",
            entity_type=EntityType.INSTITUTION,
            aliases=["Fed"],
        )
        entities = writer.write_entities([entity])
        entity_id = entities[0].entity_id

        # Write entity sentiment
        es = EntitySentiment(
            sentiment_id="sent_001",
            entity_id=entity_id,
            entity_score=0.72,
            confidence=0.88,
            label=EntitySentimentLabel.BULLISH,
            timestamp=datetime.utcnow(),
        )
        count = writer.write_entity_sentiments([es])
        assert count == 1
        assert writer.stats["entity_sentiments_written"] == 1


class TestSentimentPipeline:
    """Test the complete sentiment pipeline."""

    @pytest.fixture
    def db_engine(self):
        engine = create_engine("sqlite:///:memory:")
        with engine.connect() as conn:
            # Create all necessary tables (simplified for test)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ndip_raw_sentiment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT,
                    content_id TEXT,
                    raw_text TEXT,
                    raw_payload TEXT,
                    retrieved_at DATETIME,
                    source_metadata TEXT,
                    UNIQUE(source_id, content_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ndip_normalized_sentiment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id TEXT UNIQUE,
                    normalized_text TEXT,
                    language TEXT,
                    processed_at DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ndip_entity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_id TEXT,
                    canonical_name TEXT,
                    original_name TEXT,
                    entity_type TEXT,
                    aliases TEXT,
                    country TEXT,
                    currency TEXT,
                    created_at DATETIME,
                    UNIQUE(entity_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ndip_sentiment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentiment_id TEXT UNIQUE,
                    content_id TEXT,
                    symbol TEXT,
                    overall_score REAL,
                    confidence REAL,
                    timestamp DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ndip_sentiment_quality (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentiment_id TEXT UNIQUE,
                    quality_score REAL,
                    source_reliability REAL,
                    freshness REAL,
                    confidence REAL,
                    source_agreement REAL,
                    assessed_at DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ndip_entity_sentiment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentiment_id TEXT,
                    entity_id TEXT,
                    entity_score REAL,
                    confidence REAL,
                    label TEXT,
                    timestamp DATETIME,
                    UNIQUE(sentiment_id, entity_id)
                )
            """)
            # Warehouse tables
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_sentiment (
                    sentiment_id TEXT PRIMARY KEY,
                    source_id TEXT,
                    content_id TEXT,
                    symbol TEXT,
                    overall_score REAL,
                    confidence REAL,
                    quality_score REAL,
                    source_agreement REAL,
                    timestamp DATETIME,
                    processed_at DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dim_entity (
                    entity_id TEXT PRIMARY KEY,
                    canonical_name TEXT UNIQUE,
                    entity_type TEXT,
                    country TEXT,
                    currency TEXT,
                    aliases TEXT,
                    metadata TEXT,
                    created_at DATETIME,
                    updated_at DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_entity_sentiment (
                    fact_entity_sentiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentiment_id TEXT,
                    entity_id TEXT,
                    entity_score REAL,
                    confidence REAL,
                    label TEXT,
                    timestamp DATETIME,
                    source_entities TEXT,
                    UNIQUE(sentiment_id, entity_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_sentiment_quality (
                    sentiment_id TEXT PRIMARY KEY,
                    quality_score REAL,
                    source_reliability REAL,
                    freshness REAL,
                    confidence REAL,
                    source_agreement REAL,
                    assessed_at DATETIME
                )
            """)
            conn.commit()
        return engine

    def test_pipeline_processing(self, db_engine):
        pipeline = SentimentPipeline(db_engine)
        raw_data = {
            "source_id": "test_source",
            "source_tier": "PRIMARY",
            "content_id": "test_001",
            "text": "The Federal Reserve signals hawkish stance, USD strengthens.",
            "timestamp": datetime.utcnow().isoformat(),
            "language": "en",
            "payload": {},
            "metadata": {},
        }
        success, update = pipeline.process_item(raw_data)
        assert success
        assert update["validated"] == 1
        assert update["normalized"] == 1
        assert update["entities"] > 0
        assert update["sentiment"] == 1
        assert update["quality"] == 1
        assert update["ndip"] == 1
        assert update["warehouse"] == 1

        # Verify entity persistence
        entity_stats = pipeline.entity_writer.get_stats()
        assert entity_stats["entities_processed"] > 0
        assert entity_stats["entities_created"] > 0
        assert entity_stats["entity_sentiments_written"] > 0

    def test_backfill_idempotency(self, db_engine):
        pipeline = SentimentPipeline(db_engine)
        raw_data = {
            "source_id": "test_source",
            "content_id": "test_001",
            "text": "Sample text",
            "timestamp": datetime.utcnow().isoformat(),
        }
        # Run once
        success1, update1 = pipeline.process_item(raw_data)
        assert success1
        # Run again (should be duplicate)
        success2, update2 = pipeline.process_item(raw_data)
        assert success2  # Pipeline should skip duplicate
        assert update2["duplicates"] == 1
        # Check counters
        counters = pipeline.get_counters()
        assert counters["duplicates"] == 1


class TestSentimentFeed:
    """Test the sentiment intelligence feed."""

    @pytest.fixture
    def db_engine(self):
        engine = create_engine("sqlite:///:memory:")
        with engine.connect() as conn:
            # Create minimal tables for feed queries
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_sentiment (
                    sentiment_id TEXT PRIMARY KEY,
                    symbol TEXT,
                    overall_score REAL,
                    confidence REAL,
                    quality_score REAL,
                    source_agreement REAL,
                    timestamp DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dim_entity (
                    entity_id TEXT PRIMARY KEY,
                    canonical_name TEXT,
                    aliases TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fact_entity_sentiment (
                    entity_id TEXT,
                    entity_score REAL,
                    confidence REAL,
                    label TEXT,
                    timestamp DATETIME
                )
            """)
            # Insert some test data
            conn.execute("""
                INSERT INTO fact_sentiment (sentiment_id, symbol, overall_score, confidence, quality_score, source_agreement, timestamp)
                VALUES ('s1', 'USD', 0.68, 0.84, 0.92, 0.88, datetime('now'))
            """)
            conn.execute("""
                INSERT INTO dim_entity (entity_id, canonical_name, aliases)
                VALUES ('e1', 'Federal Reserve', '["Fed", "FED"]')
            """)
            conn.execute("""
                INSERT INTO fact_entity_sentiment (entity_id, entity_score, confidence, label, timestamp)
                VALUES ('e1', 0.72, 0.88, 'BULLISH', datetime('now'))
            """)
            conn.commit()
        return engine

    def test_get_sentiment(self, db_engine):
        feed = SentimentFeed("sqlite:///:memory:")  # Not using engine directly
        # Override engine for test
        feed.engine = db_engine
        result = feed.get_sentiment("USD")
        assert result["symbol"] == "USD"
        assert result["sentiment"] == 0.68
        assert result["label"] in [
            "VERY_BULLISH",
            "BULLISH",
            "NEUTRAL",
            "BEARISH",
            "VERY_BEARISH",
        ]
        assert result["confidence"] == 0.84

    def test_get_entity_sentiment(self, db_engine):
        feed = SentimentFeed("sqlite:///:memory:")
        feed.engine = db_engine
        result = feed.get_entity_sentiment("Federal Reserve")
        assert result["entity_name"] == "Federal Reserve"
        assert result["sentiment"] == 0.72
        assert result["label"] == "BULLISH"

    def test_get_sentiment_history(self, db_engine):
        feed = SentimentFeed("sqlite:///:memory:")
        feed.engine = db_engine
        history = feed.get_sentiment_history("USD", "1d")
        assert len(history) >= 1
        assert "timestamp" in history[0]
        assert "sentiment" in history[0]
