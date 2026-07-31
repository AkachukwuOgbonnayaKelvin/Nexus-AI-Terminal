import logging
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import statistics
import math
from collections import defaultdict

from services.asset_risk_engine.config import config

logger = logging.getLogger(__name__)

class RiskEngine:
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

    def get_risk_symbols(self):
        return [
            'US500', 'US100', 'US30',
            'GER40', 'UK100', 'FRA40',
            'HK50', 'JP225', 'AU200',
            'XAUUSD', 'CL=F', 'Copper',
            'NG=F', 'BZ=F'
        ]

    def fetch_prices(self, symbol, timeframe, limit):
        table = f"prepared.candles_{timeframe.lower()}"
        query = f"""
            SELECT timestamp, close
            FROM {table}
            WHERE symbol = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (symbol, limit))
            rows = cur.fetchall()
            return [(row['timestamp'], float(row['close'])) for row in rows]

    def compute_log_returns(self, prices):
        if len(prices) < 2:
            return []
        return [math.log(prices[i][1] / prices[i-1][1]) for i in range(1, len(prices))]

    def compute_metrics(self, symbol, timeframe, prices):
        if len(prices) < 20:
            return None

        returns = self.compute_log_returns(prices)
        if len(returns) < 20:
            return None

        # Window sizes
        if timeframe == 'D1':
            vol_window = 20
            mom_window = 20
            high_window = 60
            history_window = 252
        elif timeframe == 'W1':
            vol_window = 12
            mom_window = 12
            high_window = 26
            history_window = 104
        elif timeframe == 'MN1':
            vol_window = 6
            mom_window = 6
            high_window = 12
            history_window = 60
        else:
            vol_window = 20
            mom_window = 20
            high_window = 60
            history_window = 252

        # Current metrics
        vol = statistics.stdev(returns[-vol_window:]) if len(returns) >= vol_window else None
        momentum = (prices[0][1] - prices[mom_window][1]) / prices[mom_window][1] if len(prices) > mom_window else None
        high = max([p[1] for p in prices[:high_window]]) if len(prices) >= high_window else None
        drawdown = (prices[0][1] - high) / high if high else None

        # Volatility Z-score
        vol_history = []
        if len(returns) >= history_window:
            for i in range(history_window, 0, -vol_window):
                if i >= vol_window:
                    vol_history.append(statistics.stdev(returns[i-vol_window:i]) if len(returns[i-vol_window:i]) >= vol_window else None)
            vol_history = [v for v in vol_history if v is not None]
        if vol_history and len(vol_history) > 5:
            vol_mean = statistics.mean(vol_history)
            vol_std = statistics.stdev(vol_history)
            vol_z = (vol - vol_mean) / vol_std if vol_std > 0 else 0.0
        else:
            vol_z = 0.0

        # Trend score
        trend_score = 0.0
        if momentum is not None and drawdown is not None:
            mom_norm = max(-1, min(1, momentum * 5))
            dd_norm = max(-1, min(1, -drawdown * 10))
            trend_score = (mom_norm + dd_norm) / 2
        elif momentum is not None:
            trend_score = max(-1, min(1, momentum * 5))
        else:
            trend_score = 0.0

        # Risk score
        risk_score = 0.0
        if vol_z is not None and momentum is not None and drawdown is not None:
            mom_norm = max(-1, min(1, momentum * 5))
            dd_norm = max(-1, min(1, -drawdown * 10))
            risk_score = vol_z * 0.4 - mom_norm * 0.3 - dd_norm * 0.3
        elif vol_z is not None:
            risk_score = vol_z * 0.5
        else:
            risk_score = 0.0

        # Regime
        regime = 'NEUTRAL'
        if risk_score > 0.5 and trend_score < -0.3:
            regime = 'RISK_OFF'
        elif risk_score < -0.5 and trend_score > 0.3:
            regime = 'RISK_ON'
        elif risk_score > 0.3 and trend_score < -0.1:
            regime = 'TRANSITION'
        elif risk_score < -0.3 and trend_score > 0.1:
            regime = 'TRANSITION'

        # Confidence and data quality
        confidence = 0.8
        if len(prices) < 50:
            confidence = 0.5
            data_quality = 'INSUFFICIENT_HISTORY'
        elif vol_history and len(vol_history) < 10:
            confidence = 0.6
            data_quality = 'INSUFFICIENT_HISTORY'
        else:
            data_quality = 'GOOD'

        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'close': prices[0][1],
            'vol': vol,
            'volatility_z': vol_z,
            'momentum': momentum,
            'trend_score': trend_score,
            'drawdown': drawdown,
            'relative_strength': 0.0,
            'risk_score': risk_score,
            'regime': regime,
            'confidence': confidence,
            'data_quality': data_quality,
            'data_version': 'v1.0',
            'calculated_at': datetime.utcnow()
        }

    def run(self):
        self.connect()
        logger.info("Starting Production Risk Engine (D1, W1, MN1)")

        symbols = self.get_risk_symbols()
        timeframes = ['D1', 'W1', 'MN1']
        results = []

        for sym in symbols:
            for tf in timeframes:
                prices = self.fetch_prices(sym, tf, 300)
                if len(prices) >= 20:
                    metrics = self.compute_metrics(sym, tf, prices)
                    if metrics:
                        results.append(metrics)
                        logger.info("Processed %s %s: vol=%.4f, risk=%.2f, regime=%s", sym, tf, metrics['vol'] or 0, metrics['risk_score'], metrics['regime'])
                else:
                    results.append({
                        'symbol': sym,
                        'timeframe': tf,
                        'close': None,
                        'vol': None,
                        'volatility_z': None,
                        'momentum': None,
                        'trend_score': None,
                        'drawdown': None,
                        'relative_strength': None,
                        'risk_score': None,
                        'regime': 'UNKNOWN',
                        'confidence': 0.0,
                        'data_quality': 'INSUFFICIENT_HISTORY',
                        'data_version': 'v1.0',
                        'calculated_at': datetime.utcnow()
                    })
                    logger.warning("Insufficient data for %s %s", sym, tf)

        self.store_metrics(results)
        self.conn.close()
        logger.info("Risk Engine finished")

    def store_metrics(self, results):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS intelligence.risk_market_state_current (
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    close NUMERIC,
                    vol NUMERIC,
                    volatility_z NUMERIC,
                    momentum NUMERIC,
                    trend_score NUMERIC,
                    drawdown NUMERIC,
                    relative_strength NUMERIC,
                    risk_score NUMERIC,
                    regime TEXT,
                    confidence NUMERIC,
                    data_quality TEXT,
                    data_version TEXT,
                    calculated_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ DEFAULT NOW(),
                    PRIMARY KEY (symbol, timeframe)
                );
                CREATE TABLE IF NOT EXISTS intelligence.risk_market_state_history (
                    id SERIAL PRIMARY KEY,
                    symbol TEXT,
                    timeframe TEXT,
                    close NUMERIC,
                    vol NUMERIC,
                    volatility_z NUMERIC,
                    momentum NUMERIC,
                    trend_score NUMERIC,
                    drawdown NUMERIC,
                    relative_strength NUMERIC,
                    risk_score NUMERIC,
                    regime TEXT,
                    confidence NUMERIC,
                    data_quality TEXT,
                    data_version TEXT,
                    calculated_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS intelligence.risk_regime_current (
                    id SERIAL PRIMARY KEY,
                    global_risk_score NUMERIC,
                    global_regime TEXT,
                    confidence NUMERIC,
                    equity_contribution NUMERIC,
                    commodity_contribution NUMERIC,
                    risk_on_probability NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS intelligence.risk_regime_history (
                    id SERIAL PRIMARY KEY,
                    global_risk_score NUMERIC,
                    global_regime TEXT,
                    confidence NUMERIC,
                    equity_contribution NUMERIC,
                    commodity_contribution NUMERIC,
                    risk_on_probability NUMERIC,
                    calculated_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)

        for data in results:
            query = """
                INSERT INTO intelligence.risk_market_state_current
                (symbol, timeframe, close, vol, volatility_z, momentum, trend_score,
                 drawdown, relative_strength, risk_score, regime, confidence,
                 data_quality, data_version, calculated_at, updated_at)
                VALUES (%(symbol)s, %(timeframe)s, %(close)s, %(vol)s, %(volatility_z)s,
                        %(momentum)s, %(trend_score)s, %(drawdown)s, %(relative_strength)s,
                        %(risk_score)s, %(regime)s, %(confidence)s, %(data_quality)s,
                        %(data_version)s, %(calculated_at)s, NOW())
                ON CONFLICT (symbol, timeframe) DO UPDATE SET
                    close = EXCLUDED.close,
                    vol = EXCLUDED.vol,
                    volatility_z = EXCLUDED.volatility_z,
                    momentum = EXCLUDED.momentum,
                    trend_score = EXCLUDED.trend_score,
                    drawdown = EXCLUDED.drawdown,
                    relative_strength = EXCLUDED.relative_strength,
                    risk_score = EXCLUDED.risk_score,
                    regime = EXCLUDED.regime,
                    confidence = EXCLUDED.confidence,
                    data_quality = EXCLUDED.data_quality,
                    data_version = EXCLUDED.data_version,
                    calculated_at = EXCLUDED.calculated_at,
                    updated_at = NOW()
            """
            with self.conn.cursor() as cur:
                cur.execute(query, data)

        self.compute_global_regime()
        logger.info("Stored %d risk market states", len(results))

    def compute_global_regime(self):
        # Fetch latest per-asset states (D1 only)
        query = """
            SELECT symbol, risk_score, regime, confidence, data_quality
            FROM intelligence.risk_market_state_current
            WHERE timeframe = 'D1' AND data_quality = 'GOOD'
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        if not rows:
            logger.warning("No good D1 risk states for global regime")
            return

        weights = {
            'US500': 0.30, 'US100': 0.15, 'US30': 0.10,
            'GER40': 0.10, 'UK100': 0.05, 'FRA40': 0.05,
            'JP225': 0.10, 'HK50': 0.10, 'AU200': 0.05,
        }
        equity_score = 0.0
        commodity_contrib = 0.0
        total_weight = 0.0

        for row in rows:
            sym = row['symbol']
            # Convert Decimal to float immediately
            risk = float(row['risk_score']) if row['risk_score'] is not None else 0.0
            w = weights.get(sym, 0.0)
            if w > 0:
                equity_score += risk * w
                total_weight += w
            else:
                # commodity or other
                commodity_contrib += risk * 0.1

        if total_weight > 0:
            equity_score = equity_score / total_weight

        global_risk = equity_score * 0.7 + commodity_contrib * 0.3
        if global_risk > 0.5:
            regime = 'RISK_ON'
        elif global_risk < -0.5:
            regime = 'RISK_OFF'
        else:
            regime = 'TRANSITION'

        # Convert confidence to float as well
        confs = [float(row['confidence']) for row in rows if row['confidence'] is not None]
        avg_conf = statistics.mean(confs) if confs else 0.5
        prob = (global_risk + 1) / 2

        now = datetime.utcnow()
        data = {
            'id': 1,  # fixed id to keep only one row
            'global_risk_score': global_risk,
            'global_regime': regime,
            'confidence': avg_conf,
            'equity_contribution': equity_score,
            'commodity_contribution': commodity_contrib,
            'risk_on_probability': prob,
            'calculated_at': now
        }

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO intelligence.risk_regime_current
                (id, global_risk_score, global_regime, confidence, equity_contribution,
                 commodity_contribution, risk_on_probability, calculated_at, updated_at)
                VALUES (%(id)s, %(global_risk_score)s, %(global_regime)s, %(confidence)s,
                        %(equity_contribution)s, %(commodity_contribution)s,
                        %(risk_on_probability)s, %(calculated_at)s, NOW())
                ON CONFLICT (id) DO UPDATE SET
                    global_risk_score = EXCLUDED.global_risk_score,
                    global_regime = EXCLUDED.global_regime,
                    confidence = EXCLUDED.confidence,
                    equity_contribution = EXCLUDED.equity_contribution,
                    commodity_contribution = EXCLUDED.commodity_contribution,
                    risk_on_probability = EXCLUDED.risk_on_probability,
                    calculated_at = EXCLUDED.calculated_at,
                    updated_at = NOW()
            """, data)

        logger.info("Global risk regime: %s (score=%.2f, conf=%.2f)", regime, global_risk, avg_conf)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = RiskEngine()
    engine.run()
