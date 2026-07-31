import psycopg2
import psycopg2.extras
from datetime import datetime
from typing import List, Dict, Any

class IndexRepository:
    def __init__(self, conn):
        self.conn = conn

    def ensure_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS intelligence.currency_index_current (
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    index_value NUMERIC,
                    normalized_value NUMERIC,
                    return_1d NUMERIC,
                    return_1w NUMERIC,
                    return_1m NUMERIC,
                    momentum NUMERIC,
                    trend_score NUMERIC,
                    volatility NUMERIC,
                    rating TEXT,
                    overall_score NUMERIC,
                    confidence NUMERIC,
                    data_quality TEXT,
                    data_status TEXT,
                    fallback_from TEXT,
                    used_timeframe TEXT,
                    bars_available INTEGER,
                    bars_required INTEGER,
                    fallback_depth INTEGER,
                    confidence_multiplier NUMERIC(8,4),
                    data_quality_score NUMERIC(8,4),
                    alignment_score NUMERIC(8,4),
                    alignment_rating VARCHAR(32),
                    confidence_rating VARCHAR(32),
                    calculated_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ DEFAULT NOW(),
                    PRIMARY KEY (symbol, timeframe)
                );
                CREATE TABLE IF NOT EXISTS intelligence.currency_index_history (
                    id SERIAL PRIMARY KEY,
                    symbol TEXT,
                    timeframe TEXT,
                    index_value NUMERIC,
                    normalized_value NUMERIC,
                    return_1d NUMERIC,
                    return_1w NUMERIC,
                    return_1m NUMERIC,
                    momentum NUMERIC,
                    trend_score NUMERIC,
                    volatility NUMERIC,
                    rating TEXT,
                    overall_score NUMERIC,
                    confidence NUMERIC,
                    data_quality TEXT,
                    data_status TEXT,
                    fallback_from TEXT,
                    used_timeframe TEXT,
                    bars_available INTEGER,
                    bars_required INTEGER,
                    fallback_depth INTEGER,
                    confidence_multiplier NUMERIC(8,4),
                    data_quality_score NUMERIC(8,4),
                    alignment_score NUMERIC(8,4),
                    alignment_rating VARCHAR(32),
                    confidence_rating VARCHAR(32),
                    calculated_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

    def table_exists(self, table_name: str) -> bool:
        query = """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'prepared' AND table_name = %s
            )
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (table_name,))
            return cur.fetchone()[0]

    def get_pair_prices(self, symbol: str, timeframe: str, limit: int = 500):
        table_name = f"candles_{timeframe.lower()}"
        if not self.table_exists(table_name):
            return []
        table = f"prepared.{table_name}"
        query = f"""
            SELECT timestamp, close
            FROM {table}
            WHERE symbol = %s
            ORDER BY timestamp ASC
            LIMIT %s
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (symbol, limit))
            rows = cur.fetchall()
            return [(row['timestamp'], float(row['close'])) for row in rows]

    def upsert_index_current(self, data: Dict[str, Any]):
        required_keys = [
            'symbol', 'timeframe', 'index_value', 'normalized_value',
            'return_1d', 'return_1w', 'return_1m', 'momentum',
            'trend_score', 'volatility', 'rating', 'overall_score',
            'confidence', 'data_quality', 'data_status', 'fallback_from',
            'used_timeframe', 'bars_available', 'bars_required',
            'fallback_depth', 'confidence_multiplier', 'data_quality_score',
            'alignment_score', 'alignment_rating', 'confidence_rating',
            'calculated_at'
        ]
        for k in required_keys:
            if k not in data:
                data[k] = None

        query = """
            INSERT INTO intelligence.currency_index_current
            (symbol, timeframe, index_value, normalized_value, return_1d, return_1w, return_1m,
             momentum, trend_score, volatility, rating, overall_score, confidence,
             data_quality, data_status, fallback_from, used_timeframe,
             bars_available, bars_required,
             fallback_depth, confidence_multiplier, data_quality_score,
             alignment_score, alignment_rating, confidence_rating,
             calculated_at, updated_at)
            VALUES (
                %(symbol)s, %(timeframe)s, %(index_value)s, %(normalized_value)s,
                %(return_1d)s, %(return_1w)s, %(return_1m)s, %(momentum)s,
                %(trend_score)s, %(volatility)s, %(rating)s, %(overall_score)s,
                %(confidence)s, %(data_quality)s, %(data_status)s, %(fallback_from)s,
                %(used_timeframe)s, %(bars_available)s, %(bars_required)s,
                %(fallback_depth)s, %(confidence_multiplier)s, %(data_quality_score)s,
                %(alignment_score)s, %(alignment_rating)s, %(confidence_rating)s,
                %(calculated_at)s, NOW()
            )
            ON CONFLICT (symbol, timeframe) DO UPDATE SET
                index_value = EXCLUDED.index_value,
                normalized_value = EXCLUDED.normalized_value,
                return_1d = EXCLUDED.return_1d,
                return_1w = EXCLUDED.return_1w,
                return_1m = EXCLUDED.return_1m,
                momentum = EXCLUDED.momentum,
                trend_score = EXCLUDED.trend_score,
                volatility = EXCLUDED.volatility,
                rating = EXCLUDED.rating,
                overall_score = EXCLUDED.overall_score,
                confidence = EXCLUDED.confidence,
                data_quality = EXCLUDED.data_quality,
                data_status = EXCLUDED.data_status,
                fallback_from = EXCLUDED.fallback_from,
                used_timeframe = EXCLUDED.used_timeframe,
                bars_available = EXCLUDED.bars_available,
                bars_required = EXCLUDED.bars_required,
                fallback_depth = EXCLUDED.fallback_depth,
                confidence_multiplier = EXCLUDED.confidence_multiplier,
                data_quality_score = EXCLUDED.data_quality_score,
                alignment_score = EXCLUDED.alignment_score,
                alignment_rating = EXCLUDED.alignment_rating,
                confidence_rating = EXCLUDED.confidence_rating,
                calculated_at = EXCLUDED.calculated_at,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            cur.execute(query, data)

    def insert_history(self, data: Dict[str, Any]):
        query = """
            INSERT INTO intelligence.currency_index_history
            (symbol, timeframe, index_value, normalized_value, return_1d, return_1w, return_1m,
             momentum, trend_score, volatility, rating, overall_score, confidence,
             data_quality, data_status, fallback_from, used_timeframe,
             bars_available, bars_required,
             fallback_depth, confidence_multiplier, data_quality_score,
             alignment_score, alignment_rating, confidence_rating,
             calculated_at)
            VALUES (
                %(symbol)s, %(timeframe)s, %(index_value)s, %(normalized_value)s,
                %(return_1d)s, %(return_1w)s, %(return_1m)s, %(momentum)s,
                %(trend_score)s, %(volatility)s, %(rating)s, %(overall_score)s,
                %(confidence)s, %(data_quality)s, %(data_status)s, %(fallback_from)s,
                %(used_timeframe)s, %(bars_available)s, %(bars_required)s,
                %(fallback_depth)s, %(confidence_multiplier)s, %(data_quality_score)s,
                %(alignment_score)s, %(alignment_rating)s, %(confidence_rating)s,
                %(calculated_at)s
            )
        """
        with self.conn.cursor() as cur:
            cur.execute(query, data)
