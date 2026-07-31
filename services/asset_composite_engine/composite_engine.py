import logging
import psycopg2
import psycopg2.extras
from datetime import datetime

from services.asset_composite_engine.config import config

logger = logging.getLogger(__name__)

class CompositeEngine:
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

    def fetch_technical_scores(self):
        query = "SELECT currency, technical_score FROM intelligence.currency_strength_current"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return {row['currency']: float(row['technical_score']) if row['technical_score'] is not None else 0.0 for row in cur.fetchall()}

    def fetch_macro_scores(self):
        query = "SELECT currency, score FROM intelligence.macro_scores_current"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return {row['currency']: float(row['score']) if row['score'] is not None else 0.0 for row in cur.fetchall()}

    def fetch_intermarket_scores(self):
        query = "SELECT currency, score FROM intelligence.intermarket_scores_current"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return {row['currency']: float(row['score']) if row['score'] is not None else 0.0 for row in cur.fetchall()}

    def fetch_monetary_scores(self):
        query = "SELECT currency, score FROM intelligence.monetary_scores_current"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return {row['currency']: float(row['score']) if row['score'] is not None else 0.0 for row in cur.fetchall()}

    def compute_composite(self, tech_scores, macro_scores, intermarket_scores, monetary_scores):
        currencies = set(tech_scores.keys()) | set(macro_scores.keys()) | set(intermarket_scores.keys()) | set(monetary_scores.keys())
        results = {}
        for curr in currencies:
            tech = tech_scores.get(curr, 0.0)
            macro = macro_scores.get(curr, 0.0)
            intermarket = intermarket_scores.get(curr, 0.0)
            monetary = monetary_scores.get(curr, 0.0)

            weighted_sum = (tech * config.weights['technical'] +
                            macro * config.weights['macro'] +
                            intermarket * config.weights['intermarket'] +
                            monetary * config.weights['monetary'])
            total_weight = (config.weights['technical'] +
                            config.weights['macro'] +
                            config.weights['intermarket'] +
                            config.weights['monetary'])
            composite = weighted_sum / total_weight if total_weight > 0 else 0.0

            results[curr] = {
                'composite': composite,
                'technical_score': tech,
                'macro_score': macro,
                'intermarket_score': intermarket,
                'monetary_score': monetary,
                'micro_score': None,
                'risk_score': None,
                'cot_score': None,
                'regime': 'BULLISH' if composite > 0.5 else 'BEARISH' if composite < -0.5 else 'NEUTRAL',
                'confidence': 0.5 + abs(composite) / 2.0
            }
        return results

    def update_strength_current(self, results):
        now = datetime.utcnow()
        records = []
        for currency, data in results.items():
            records.append({
                'currency': currency,
                'score': data['composite'],
                'technical_score': data['technical_score'],
                'macro_score': data['macro_score'],
                'micro_score': data['micro_score'],
                'monetary_score': data['monetary_score'],
                'intermarket_score': data['intermarket_score'],
                'risk_score': data['risk_score'],
                'cot_score': data['cot_score'],
                'regime': data['regime'],
                'confidence': data['confidence'],
                'calculated_at': now,
                'status': 'COMPOSITE'
            })

        query = """
            INSERT INTO intelligence.currency_strength_current (
                currency, score, technical_score, macro_score,
                micro_score, monetary_score, intermarket_score,
                risk_score, cot_score, regime, confidence,
                calculated_at, status, updated_at
            ) VALUES (
                %(currency)s, %(score)s, %(technical_score)s, %(macro_score)s,
                %(micro_score)s, %(monetary_score)s, %(intermarket_score)s,
                %(risk_score)s, %(cot_score)s, %(regime)s, %(confidence)s,
                %(calculated_at)s, %(status)s, NOW()
            )
            ON CONFLICT (currency) DO UPDATE SET
                score = EXCLUDED.score,
                technical_score = EXCLUDED.technical_score,
                macro_score = EXCLUDED.macro_score,
                micro_score = EXCLUDED.micro_score,
                monetary_score = EXCLUDED.monetary_score,
                intermarket_score = EXCLUDED.intermarket_score,
                risk_score = EXCLUDED.risk_score,
                cot_score = EXCLUDED.cot_score,
                regime = EXCLUDED.regime,
                confidence = EXCLUDED.confidence,
                calculated_at = EXCLUDED.calculated_at,
                status = EXCLUDED.status,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, records)
        logger.info("Updated %d currency strength records", len(records))

    def run(self):
        self.connect()
        logger.info("Starting Composite Engine")

        tech_scores = self.fetch_technical_scores()
        macro_scores = self.fetch_macro_scores()
        intermarket_scores = self.fetch_intermarket_scores()
        monetary_scores = self.fetch_monetary_scores()
        logger.info("Fetched technical: %d, macro: %d, intermarket: %d, monetary: %d",
                    len(tech_scores), len(macro_scores), len(intermarket_scores), len(monetary_scores))

        results = self.compute_composite(tech_scores, macro_scores, intermarket_scores, monetary_scores)
        logger.info("Computed composite for %d currencies", len(results))

        if results:
            self.update_strength_current(results)

        self.conn.close()
        logger.info("Composite Engine finished")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = CompositeEngine()
    engine.run()
