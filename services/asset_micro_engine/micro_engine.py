import logging
import psycopg2
import psycopg2.extras
from datetime import datetime
from collections import defaultdict

from services.asset_micro_engine.config import config

logger = logging.getLogger(__name__)

class MicroEngine:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=config.asset_host,
            port=config.asset_port,
            dbname=config.asset_dbname,
            user=config.asset_user,
            password=config.asset_password
        )
        self.conn.autocommit = True
        logger.info("Connected to asset database")

    def fetch_micro_events(self):
        """
        Fetch economic events that are classified as 'micro' based on category/subcategory.
        We define micro as: consumer, labor, business, housing, retail, sentiment.
        """
        micro_keywords = ['consumer', 'labor', 'business', 'housing', 'retail', 'sentiment', 'pmi', 'claims']
        # Since we don't have category/subcategory populated yet, we'll filter by title keywords.
        # For a more robust solution, we should add a category column or use a mapping.
        query = """
            SELECT
                currency,
                title,
                actual,
                forecast,
                previous,
                importance,
                release_time_utc
            FROM raw.economic_events
            WHERE actual IS NOT NULL
              AND (category ILIKE ANY(%s) OR subcategory ILIKE ANY(%s) OR title ILIKE ANY(%s))
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (micro_keywords, micro_keywords, micro_keywords))
            return cur.fetchall()

    def compute_micro_score(self, events):
        """
        Compute a micro score per currency based on the direction and magnitude of recent indicators.
        Since we lack forecast/previous, we'll use a simple proxy: compare actual to a moving average
        or simply treat the actual value itself as a score (normalized).
        For now, we'll assign a neutral 0.0 as placeholder until real data arrives.
        """
        # Placeholder: return 0 for all currencies
        # In a real implementation, we would compute surprise (actual - forecast) once available.
        currencies = set([evt['currency'] for evt in events if evt['currency']])
        if not currencies:
            logger.info("No micro events found")
            return {}

        scores = {}
        for curr in currencies:
            scores[curr] = {
                'score': 0.0,  # placeholder
                'calculated_at': datetime.utcnow()
            }
        return scores

    def store_scores(self, scores):
        # Create tables if not exists
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS intelligence.micro_scores_current (
                    currency TEXT PRIMARY KEY,
                    score NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS intelligence.micro_scores_history (
                    id SERIAL PRIMARY KEY,
                    currency TEXT,
                    score NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

        records = []
        for currency, data in scores.items():
            records.append({
                'currency': currency,
                'score': data['score'],
                'calculated_at': data['calculated_at']
            })

        query_current = """
            INSERT INTO intelligence.micro_scores_current
            (currency, score, calculated_at, updated_at)
            VALUES (%(currency)s, %(score)s, %(calculated_at)s, NOW())
            ON CONFLICT (currency) DO UPDATE SET
                score = EXCLUDED.score,
                calculated_at = EXCLUDED.calculated_at,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_current, records)

        query_history = """
            INSERT INTO intelligence.micro_scores_history
            (currency, score, calculated_at)
            VALUES (%(currency)s, %(score)s, %(calculated_at)s)
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_history, records)

        logger.info("Stored micro scores for %d currencies", len(records))

    def run(self):
        self.connect()
        logger.info("Starting Micro Engine")

        events = self.fetch_micro_events()
        logger.info("Fetched %d micro events", len(events))

        scores = self.compute_micro_score(events)
        logger.info("Computed micro scores for %d currencies", len(scores))

        if scores:
            self.store_scores(scores)

        self.conn.close()
        logger.info("Micro Engine finished")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = MicroEngine()
    engine.run()
