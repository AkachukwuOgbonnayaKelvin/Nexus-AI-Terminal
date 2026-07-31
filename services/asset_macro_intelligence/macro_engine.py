import logging
from datetime import datetime
import psycopg2
import psycopg2.extras
from collections import defaultdict

from services.asset_macro_intelligence.config import config

logger = logging.getLogger(__name__)

class MacroIntelligenceEngine:
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

    def fetch_economic_events(self):
        """Fetch economic events from raw.economic_events."""
        query = """
            SELECT
                event_id, country, currency, title, category,
                forecast, previous, actual, importance,
                release_time_utc, metadata
            FROM raw.economic_events
            WHERE actual IS NOT NULL
            ORDER BY release_time_utc DESC
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def calculate_surprise(self, event):
        """Calculate surprise (actual vs forecast, fallback to actual vs previous)."""
        if event['forecast'] is not None:
            return event['actual'] - event['forecast']
        elif event['previous'] is not None:
            return event['actual'] - event['previous']
        return None

    def determine_direction(self, event, surprise):
        """
        Determine if the surprise is bullish or bearish for the currency.
        This is a simplified mapping; in production we need indicator-specific logic.
        """
        if surprise is None:
            return 'neutral'
        # Assume higher than expected is bullish for most indicators
        # In a real system, we need a mapping per indicator
        return 'bullish' if surprise > 0 else 'bearish'

    def compute_macro_score(self, events):
        """
        Compute a macro score per currency based on recent economic events.
        """
        # Group events by currency
        currency_events = defaultdict(list)
        for evt in events:
            if evt['currency']:
                currency_events[evt['currency']].append(evt)

        scores = {}
        for currency, evts in currency_events.items():
            total_score = 0.0
            total_weight = 0.0
            components = []

            for evt in evts:
                surprise = self.calculate_surprise(evt)
                if surprise is None:
                    continue
                direction = self.determine_direction(evt, surprise)
                importance = evt['importance'] if evt['importance'] else 3  # default medium
                # Normalize importance to 1-5 scale
                if importance == 'low':
                    imp = 1
                elif importance == 'medium' or importance == 'moderate':
                    imp = 3
                elif importance == 'high':
                    imp = 5
                else:
                    try:
                        imp = float(importance)
                    except:
                        imp = 3
                # Surprise magnitude (normalized)
                mag = abs(surprise) / (abs(evt['previous']) + 1e-6) if evt['previous'] else abs(surprise)
                # Contribution: direction * (surprise magnitude * importance)
                contrib = (1 if direction == 'bullish' else -1) * mag * imp / 5.0
                total_score += contrib
                total_weight += imp
                components.append({
                    'title': evt['title'],
                    'surprise': surprise,
                    'direction': direction,
                    'importance': imp,
                    'contribution': contrib
                })

            if total_weight > 0:
                avg_score = total_score / total_weight
            else:
                avg_score = 0.0

            scores[currency] = {
                'score': avg_score,
                'components': components,
                'event_count': len(evts)
            }

        return scores

    def store_scores(self, scores):
        """Store macro scores in intelligence schema."""
        if not scores:
            return 0

        now = datetime.utcnow()
        records = []
        for currency, data in scores.items():
            records.append({
                'currency': currency,
                'score': data['score'],
                'components': psycopg2.extras.Json(data['components']),
                'calculated_at': now
            })

        # Update current table
        query_current = """
            INSERT INTO intelligence.macro_scores_current (currency, score, components, calculated_at, updated_at)
            VALUES (%(currency)s, %(score)s, %(components)s, %(calculated_at)s, NOW())
            ON CONFLICT (currency) DO UPDATE SET
                score = EXCLUDED.score,
                components = EXCLUDED.components,
                calculated_at = EXCLUDED.calculated_at,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_current, records)

        # Insert into history
        query_history = """
            INSERT INTO intelligence.macro_scores_history (currency, score, components, calculated_at)
            VALUES (%(currency)s, %(score)s, %(components)s, %(calculated_at)s)
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_history, records)

        return len(records)

    def run(self):
        self.connect()
        logger.info("Starting Macro Intelligence Engine")
        events = self.fetch_economic_events()
        logger.info("Fetched %d economic events", len(events))
        scores = self.compute_macro_score(events)
        logger.info("Computed macro scores for %d currencies", len(scores))
        if scores:
            count = self.store_scores(scores)
            logger.info("Stored macro scores for %d currencies", count)
        else:
            logger.info("No scores to store")
        self.conn.close()
        logger.info("Macro Intelligence Engine finished")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = MacroIntelligenceEngine()
    engine.run()
