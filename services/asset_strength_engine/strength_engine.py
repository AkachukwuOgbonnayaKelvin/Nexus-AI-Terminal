import logging
from datetime import datetime
import psycopg2
import psycopg2.extras
from collections import defaultdict

from services.asset_strength_engine.config import config
from services.asset_strength_engine.repositories.prepared_candle_repository import PreparedCandleRepository

logger = logging.getLogger(__name__)

class CurrencyStrengthEngine:
    def __init__(self):
        self.conn = None
        self.repo = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=config.asset_host,
            port=config.asset_port,
            dbname=config.asset_dbname,
            user=config.asset_user,
            password=config.asset_password
        )
        self.conn.autocommit = True
        self.repo = PreparedCandleRepository(self.conn)
        logger.info("Connected to asset database: %s", config.asset_dbname)

    def map_symbol_to_currency(self, symbol):
        """
        Extract base currency from forex symbols (first 3 chars).
        For indices/commodities, skip.
        """
        base = symbol[:3]
        if base in ['EUR', 'GBP', 'USD', 'JPY', 'AUD', 'NZD', 'CAD', 'CHF']:
            return base
        return None

    def calculate_z_score(self, prices):
        if len(prices) < 10:
            return None
        mean = sum(prices) / len(prices)
        std = (sum((x - mean)**2 for x in prices) / len(prices)) ** 0.5
        if std == 0:
            return None
        return (prices[-1] - mean) / std

    def compute_scores(self):
        # Collect symbols per currency
        currency_symbols = defaultdict(set)
        for tf in config.timeframes:
            symbols = self.repo.get_symbols(tf)
            for sym in symbols:
                curr = self.map_symbol_to_currency(sym)
                if curr:
                    currency_symbols[curr].add(sym)

        results = {}
        for currency, sym_set in currency_symbols.items():
            scores = {}
            for tf in config.timeframes:
                z_values = []
                for sym in sym_set:
                    prices = self.repo.get_closing_prices(sym, tf, config.lookback[tf])
                    if len(prices) >= 10:
                        z = self.calculate_z_score(prices)
                        if z is not None:
                            z_values.append(z)
                if z_values:
                    avg_z = sum(z_values) / len(z_values)
                    scores[tf] = avg_z
                else:
                    scores[tf] = None

            # Composite
            composite = 0.0
            total_weight = 0.0
            for tf, score in scores.items():
                if score is not None:
                    composite += score * config.weights.get(tf, 0)
                    total_weight += config.weights.get(tf, 0)
            composite = composite / total_weight if total_weight > 0 else None

            results[currency] = {
                'scores': scores,
                'composite': composite,
            }

        return results

    def store_scores(self, results):
        if not results:
            return 0

        now = datetime.utcnow()
        records = []
        for currency, data in results.items():
            row = {
                'currency': currency,
                'timestamp': now,
                'score': data['composite'],
                'm15_score': data['scores'].get('M15'),
                'h1_score': data['scores'].get('H1'),
                'h4_score': data['scores'].get('H4'),
                'd1_score': data['scores'].get('D1'),
                'w1_score': data['scores'].get('W1'),
                'mn1_score': data['scores'].get('MN1'),
                'regime': 'BULLISH' if data['composite'] and data['composite'] > 0.5 else 'BEARISH' if data['composite'] and data['composite'] < -0.5 else 'NEUTRAL',
            }
            records.append(row)

        # Insert into history
        hist_query = """
            INSERT INTO intelligence.currency_strength_history (
                currency, timestamp, score, technical_score,
                macro_score, micro_score, monetary_score, intermarket_score,
                risk_score, cot_score, velocity, acceleration,
                regime, confidence, data_version, status
            ) VALUES (
                %(currency)s, %(timestamp)s, %(score)s,
                NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                NULL, NULL, %(regime)s, NULL, NULL, 'TECHNICAL_ONLY'
            )
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, hist_query, records)

        # Upsert into current
        curr_query = """
            INSERT INTO intelligence.currency_strength_current (
                currency, score, technical_score, macro_score, micro_score,
                monetary_score, intermarket_score, risk_score, cot_score,
                velocity, acceleration, regime, confidence, data_version,
                status, calculated_at, updated_at
            ) VALUES (
                %(currency)s, %(score)s, %(score)s, NULL, NULL,
                NULL, NULL, NULL, NULL,
                NULL, NULL, %(regime)s, NULL, NULL,
                'TECHNICAL_ONLY', %(timestamp)s, NOW()
            )
            ON CONFLICT (currency) DO UPDATE SET
                score = EXCLUDED.score,
                technical_score = EXCLUDED.technical_score,
                regime = EXCLUDED.regime,
                status = EXCLUDED.status,
                calculated_at = EXCLUDED.calculated_at,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, curr_query, records)

        return len(records)

    def run(self):
        self.connect()
        logger.info("Starting Technical Strength Engine")
        results = self.compute_scores()
        if results:
            count = self.store_scores(results)
            logger.info("Stored scores for %d currencies", count)
        else:
            logger.info("No scores computed")
        self.conn.close()
        logger.info("Engine finished")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = CurrencyStrengthEngine()
    engine.run()
