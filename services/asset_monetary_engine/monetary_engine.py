import logging
import psycopg2
import psycopg2.extras
from datetime import datetime
import statistics

from services.asset_monetary_engine.config import config

logger = logging.getLogger(__name__)

class MonetaryEngine:
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

    def fetch_latest_rates(self):
        """
        Fetch the most recent central bank event for each currency with a new_rate.
        """
        query = """
            SELECT DISTINCT ON (currency)
                currency,
                new_rate,
                old_rate,
                rate_change,
                release_time,
                policy_bias,
                hawkish_dovish_score
            FROM raw.central_bank_events
            WHERE new_rate IS NOT NULL
            ORDER BY currency, release_time DESC
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def compute_scores(self, events):
        """
        Compute monetary score per currency based on rate level and changes.
        """
        # Extract rate levels
        rate_levels = {}
        rate_changes = {}
        for evt in events:
            curr = evt['currency']
            rate = float(evt['new_rate']) if evt['new_rate'] is not None else None
            if rate is not None:
                rate_levels[curr] = rate
            # Rate change
            if evt['rate_change'] is not None:
                rate_changes[curr] = float(evt['rate_change'])
            elif evt['old_rate'] is not None and evt['new_rate'] is not None:
                rate_changes[curr] = float(evt['new_rate']) - float(evt['old_rate'])

        # Z-score of rate levels
        rates = list(rate_levels.values())
        if len(rates) < 2:
            logger.warning("Not enough rate data to compute Z-score")
            mean = 0.0
            std = 1.0
        else:
            mean = statistics.mean(rates)
            std = statistics.stdev(rates) if len(rates) > 1 else 1.0

        scores = {}
        for curr, rate in rate_levels.items():
            z = (rate - mean) / std if std > 0 else 0.0
            # Add change contribution (if available)
            change = rate_changes.get(curr, 0.0)
            # Normalize change: a rate hike is bullish (positive), cut is bearish (negative)
            # We'll scale it by 0.5 to avoid dominating the score
            change_contrib = change * 0.5  # e.g., +0.25% hike adds +0.125 to score
            total = z + change_contrib
            scores[curr] = {
                'rate_level_z': z,
                'rate_change': change,
                'change_contribution': change_contrib,
                'score': total,
                'calculated_at': datetime.utcnow()
            }

        # Ensure all major currencies are present (set default if missing)
        major_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD']
        for curr in major_currencies:
            if curr not in scores:
                scores[curr] = {
                    'rate_level_z': 0.0,
                    'rate_change': 0.0,
                    'change_contribution': 0.0,
                    'score': 0.0,
                    'calculated_at': datetime.utcnow()
                }

        return scores

    def store_scores(self, scores):
        # Create tables if not exists
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS intelligence.monetary_scores_current (
                    currency TEXT PRIMARY KEY,
                    score NUMERIC,
                    rate_level_z NUMERIC,
                    rate_change_contribution NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS intelligence.monetary_scores_history (
                    id SERIAL PRIMARY KEY,
                    currency TEXT,
                    score NUMERIC,
                    rate_level_z NUMERIC,
                    rate_change_contribution NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

        records = []
        for currency, data in scores.items():
            records.append({
                'currency': currency,
                'score': data['score'],
                'rate_level_z': data['rate_level_z'],
                'rate_change_contribution': data['change_contribution'],
                'calculated_at': data['calculated_at']
            })

        query_current = """
            INSERT INTO intelligence.monetary_scores_current
            (currency, score, rate_level_z, rate_change_contribution, calculated_at, updated_at)
            VALUES (%(currency)s, %(score)s, %(rate_level_z)s, %(rate_change_contribution)s, %(calculated_at)s, NOW())
            ON CONFLICT (currency) DO UPDATE SET
                score = EXCLUDED.score,
                rate_level_z = EXCLUDED.rate_level_z,
                rate_change_contribution = EXCLUDED.rate_change_contribution,
                calculated_at = EXCLUDED.calculated_at,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_current, records)

        query_history = """
            INSERT INTO intelligence.monetary_scores_history
            (currency, score, rate_level_z, rate_change_contribution, calculated_at)
            VALUES (%(currency)s, %(score)s, %(rate_level_z)s, %(rate_change_contribution)s, %(calculated_at)s)
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_history, records)

        logger.info("Stored monetary scores for %d currencies", len(records))

    def run(self):
        self.connect()
        logger.info("Starting Monetary Engine")

        events = self.fetch_latest_rates()
        logger.info("Fetched %d latest rate events", len(events))

        scores = self.compute_scores(events)
        logger.info("Computed monetary scores for %d currencies", len(scores))

        if scores:
            self.store_scores(scores)

        self.conn.close()
        logger.info("Monetary Engine finished")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = MonetaryEngine()
    engine.run()
