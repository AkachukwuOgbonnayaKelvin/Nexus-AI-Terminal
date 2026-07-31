import logging
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

from services.asset_intermarket_engine.config import config

logger = logging.getLogger(__name__)

class IntermarketEngine:
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

    def fetch_price_data(self, symbol, timeframe='D1', limit=60):
        """Fetch recent prices for a symbol from prepared candles."""
        # Use D1 table
        query = """
            SELECT timestamp, close
            FROM prepared.candles_d1
            WHERE symbol = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (symbol, limit))
            rows = cur.fetchall()
            return [(row['timestamp'], float(row['close'])) for row in rows]

    def compute_returns(self, prices):
        """Compute percentage returns from a list of prices."""
        if len(prices) < 2:
            return []
        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i][1] - prices[i-1][1]) / prices[i-1][1]
            returns.append(ret)
        return returns

    def get_intermarket_assets(self):
        """Define intermarket assets and currency sensitivities."""
        # We'll use equity indices and commodities
        assets = {
            'equity': ['US500', 'GER40', 'UK100'],
            'commodity': ['XAUUSD', 'CL=F'],  # gold and crude oil
        }
        # Risk sensitivity (positive = risk-on)
        risk_mapping = {
            'AUD': 1.0,
            'NZD': 1.0,
            'CAD': 0.8,
            'GBP': 0.6,
            'EUR': 0.6,
            'USD': -0.5,
            'CHF': -0.8,
            'JPY': -0.9,
        }
        # Commodity sensitivity
        commodity_mapping = {
            'CAD': 1.0,  # oil
            'AUD': 1.0,  # gold/copper
            'NZD': 0.5,
            'CHF': 0.5,  # gold
            'USD': 0.2,
            'EUR': 0.1,
            'GBP': 0.1,
            'JPY': 0.1,
        }
        return assets, risk_mapping, commodity_mapping

    def run(self):
        self.connect()
        logger.info("Starting Intermarket Engine")

        assets, risk_mapping, commodity_mapping = self.get_intermarket_assets()

        # Fetch data for each asset
        asset_returns = {}
        for asset_type, symbols in assets.items():
            for sym in symbols:
                prices = self.fetch_price_data(sym, 'D1', 60)
                if len(prices) < 30:
                    logger.warning(f"Not enough data for {sym} (got {len(prices)})")
                    continue
                rets = self.compute_returns(prices)
                if rets:
                    # Recent 5-day return
                    recent_ret = sum(rets[-5:]) / 5
                    asset_returns[sym] = {'recent_ret': recent_ret, 'returns': rets}

        if not asset_returns:
            logger.error("No intermarket asset data available")
            return

        # Compute risk factor (average of equity returns)
        equity_returns = [asset_returns[sym]['recent_ret'] for sym in assets['equity'] if sym in asset_returns]
        risk_factor = statistics.mean(equity_returns) if equity_returns else 0.0

        # Compute commodity factor
        commodity_returns = [asset_returns[sym]['recent_ret'] for sym in assets['commodity'] if sym in asset_returns]
        commodity_factor = statistics.mean(commodity_returns) if commodity_returns else 0.0

        # Compute scores per currency
        currencies = set(risk_mapping.keys()) | set(commodity_mapping.keys())
        scores = {}
        for curr in currencies:
            risk_score = risk_factor * risk_mapping.get(curr, 0)
            comm_score = commodity_factor * commodity_mapping.get(curr, 0)
            total = risk_score + comm_score
            scores[curr] = {
                'score': total,
                'risk_contribution': risk_score,
                'commodity_contribution': comm_score,
                'calculated_at': datetime.utcnow()
            }

        # Store results
        self.store_scores(scores)
        logger.info("Intermarket Engine finished")

    def store_scores(self, scores):
        # Create tables if not exists
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS intelligence.intermarket_scores_current (
                    currency TEXT PRIMARY KEY,
                    score NUMERIC,
                    risk_contribution NUMERIC,
                    commodity_contribution NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS intelligence.intermarket_scores_history (
                    id SERIAL PRIMARY KEY,
                    currency TEXT,
                    score NUMERIC,
                    risk_contribution NUMERIC,
                    commodity_contribution NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

        records = []
        now = datetime.utcnow()
        for currency, data in scores.items():
            records.append({
                'currency': currency,
                'score': data['score'],
                'risk_contribution': data['risk_contribution'],
                'commodity_contribution': data['commodity_contribution'],
                'calculated_at': data['calculated_at']
            })

        query_current = """
            INSERT INTO intelligence.intermarket_scores_current
            (currency, score, risk_contribution, commodity_contribution, calculated_at, updated_at)
            VALUES (%(currency)s, %(score)s, %(risk_contribution)s, %(commodity_contribution)s, %(calculated_at)s, NOW())
            ON CONFLICT (currency) DO UPDATE SET
                score = EXCLUDED.score,
                risk_contribution = EXCLUDED.risk_contribution,
                commodity_contribution = EXCLUDED.commodity_contribution,
                calculated_at = EXCLUDED.calculated_at,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_current, records)

        query_history = """
            INSERT INTO intelligence.intermarket_scores_history
            (currency, score, risk_contribution, commodity_contribution, calculated_at)
            VALUES (%(currency)s, %(score)s, %(risk_contribution)s, %(commodity_contribution)s, %(calculated_at)s)
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query_history, records)

        logger.info("Stored intermarket scores for %d currencies", len(records))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = IntermarketEngine()
    engine.run()
