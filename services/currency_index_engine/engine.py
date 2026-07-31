from __future__ import annotations

import logging
import math
import statistics
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple

import psycopg2

from services.currency_index_engine.config import config
from services.currency_index_engine.baskets import BASKETS
from services.currency_index_engine.repository import IndexRepository
from services.currency_index_engine.rating import compute_rating

logger = logging.getLogger(__name__)


@dataclass
class TimeframeResult:
    requested_timeframe: str
    used_timeframe: str
    score: Optional[float]
    status: str
    bars_available: int
    bars_required: int
    fallback_depth: int = 0
    confidence_multiplier: float = 0.0
    data_quality_score: float = 0.0


@dataclass
class TimeframeEvidence:
    requested_timeframe: str
    source_timeframe: Optional[str]
    score: Optional[float]
    data_status: str
    fallback_depth: int
    confidence_multiplier: float
    data_quality_score: float
    bars_available: int = 0
    bars_required: int = 0

    @property
    def is_usable(self) -> bool:
        return (
            self.score is not None
            and self.data_status in {"VALID", "FALLBACK"}
            and self.confidence_multiplier > 0
        )

    @property
    def source_key(self) -> Optional[str]:
        return self.source_timeframe or self.requested_timeframe


class CurrencyIndexEngine:
    def __init__(self):
        self.conn = None
        self.repo = None
        self.all_results = {}  # symbol -> {timeframe -> TimeframeResult}

    def connect(self):
        self.conn = psycopg2.connect(
            host=config.asset_host,
            port=config.asset_port,
            dbname=config.asset_dbname,
            user=config.asset_user,
            password=config.asset_password
        )
        self.conn.autocommit = True
        self.repo = IndexRepository(self.conn)
        self.repo.ensure_tables()
        logger.info("Connected to asset database")

    def get_pair_prices_for_date(self, symbol: str, timeframe: str, date: datetime) -> float:
        query = f"""
            SELECT close
            FROM prepared.candles_{timeframe.lower()}
            WHERE symbol = %s AND timestamp <= %s
            ORDER BY timestamp DESC
            LIMIT 1
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (symbol, date))
            row = cur.fetchone()
            if row:
                return float(row[0])
            return None

    def compute_index_value(self, pairs, timeframe, date):
        numerator = 1.0
        denominator = 1.0
        valid = 0
        for symbol, role in pairs:
            price = self.get_pair_prices_for_date(symbol, timeframe, date)
            if price is None or price <= 0:
                return None
            if role == 'num':
                numerator *= price
            else:
                denominator *= price
            valid += 1
        if valid == 0 or denominator == 0:
            return None
        n = len(pairs)
        return (numerator / denominator) ** (1.0 / n)

    def compute_metrics(self, values):
        if len(values) < 2:
            return {}
        return_1d = (values[-1] - values[-2]) / values[-2] if len(values) >= 2 else None
        return_1w = (values[-1] - values[-7]) / values[-7] if len(values) >= 7 else None
        return_1m = (values[-1] - values[-30]) / values[-30] if len(values) >= 30 else None
        momentum = (values[-1] - values[-20]) / values[-20] if len(values) >= 20 else None
        trend_score = 0.0
        if len(values) >= 20:
            x = list(range(len(values[-20:])))
            y = values[-20:]
            n = len(x)
            sum_x = sum(x)
            sum_y = sum(y)
            sum_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
            sum_x2 = sum(x_i**2 for x_i in x)
            denom = n * sum_x2 - sum_x**2
            if denom != 0:
                slope = (n * sum_xy - sum_x * sum_y) / denom
                trend_score = min(100, max(-100, slope * 1000))
        returns = [(values[i] - values[i-1]) / values[i-1] for i in range(1, len(values))]
        vol = statistics.stdev(returns[-20:]) if len(returns) >= 20 else None
        return {
            'return_1d': return_1d,
            'return_1w': return_1w,
            'return_1m': return_1m,
            'momentum': momentum,
            'trend_score': trend_score,
            'volatility': vol,
        }

    def compute_timeframe_score(self, values, metrics):
        trend = metrics.get('trend_score', 0)
        mom = metrics.get('momentum', 0) * 100 if metrics.get('momentum') is not None else 0
        vol = metrics.get('volatility')
        vol_adj = 0.0
        if vol is not None:
            vol_adj = max(-20, min(20, (0.015 - vol) * 2000))
        score = trend * 0.5 + mom * 0.3 + vol_adj * 0.2
        return max(-100, min(100, score))

    def _calculate_timeframe(self, idx_name, pairs, timeframe):
        """Compute score for a specific timeframe, returns (score, bars_available) or None."""
        timestamps = []
        for symbol, _ in pairs:
            prices = self.repo.get_pair_prices(symbol, timeframe, 500)
            if prices:
                timestamps.extend([t for t, _ in prices])
        if not timestamps:
            return None

        min_date = min(timestamps)
        max_date = max(timestamps)
        step = timedelta(days=30) if timeframe == 'MN1' else timedelta(days=7) if timeframe == 'W1' else timedelta(days=1)

        date_list = []
        current = min_date
        while current <= max_date:
            date_list.append(current)
            current += step

        index_values = []
        for dt in date_list:
            val = self.compute_index_value(pairs, timeframe, dt)
            if val is not None:
                index_values.append(val)

        bars_available = len(index_values)
        bars_required = config.timeframe_config.get(timeframe, {}).get('minimum_bars', 20)
        if bars_available < bars_required:
            return None

        base = index_values[0] if index_values else 1
        normalized_values = [v / base * 100 for v in index_values]
        metrics = self.compute_metrics(normalized_values)
        score = self.compute_timeframe_score(normalized_values, metrics)
        return score, bars_available

    def resolve_timeframe(self, idx_name, pairs, requested_tf) -> TimeframeResult:
        """Resolve a timeframe with fallback, returning a TimeframeResult."""
        cfg = config.timeframe_config.get(requested_tf, {})
        required = cfg.get('minimum_bars', 20)

        # Try direct
        direct = self._calculate_timeframe(idx_name, pairs, requested_tf)
        if direct is not None:
            score, bars = direct
            return TimeframeResult(
                requested_timeframe=requested_tf,
                used_timeframe=requested_tf,
                score=score,
                status='VALID',
                bars_available=bars,
                bars_required=required,
                fallback_depth=0,
                confidence_multiplier=1.0,
                data_quality_score=100.0,
            )

        # Try fallbacks
        fallbacks = config.fallback_chain.get(requested_tf, [])
        for depth, fb_tf in enumerate(fallbacks, start=1):
            fb = self._calculate_timeframe(idx_name, pairs, fb_tf)
            if fb is not None:
                score, bars = fb
                # Confidence multiplier decreases with depth
                base_mult = config.data_status_weight.get('FALLBACK', 0.55)
                mult = base_mult ** depth
                quality = mult * 100
                return TimeframeResult(
                    requested_timeframe=requested_tf,
                    used_timeframe=fb_tf,
                    score=score,
                    status='FALLBACK',
                    bars_available=bars,
                    bars_required=required,
                    fallback_depth=depth,
                    confidence_multiplier=mult,
                    data_quality_score=quality,
                )

        # No data
        return TimeframeResult(
            requested_timeframe=requested_tf,
            used_timeframe=requested_tf,
            score=None,
            status='NO_DATA',
            bars_available=0,
            bars_required=required,
            fallback_depth=0,
            confidence_multiplier=0.0,
            data_quality_score=0.0,
        )

    # ------------------------------------------------------------------
    # NEW: INSTITUTIONAL AGGREGATION LAYER
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_float(value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            result = float(value)
            if not math.isfinite(result):
                return None
            return result
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
        return max(low, min(high, value))

    @staticmethod
    def _rating_from_score(score: Optional[float]) -> str:
        if score is None:
            return "NO_DATA"
        if score >= 60:
            return "STRONG_BUY"
        if score >= 20:
            return "WEAK_BUY"
        if score <= -60:
            return "STRONG_SELL"
        if score <= -20:
            return "WEAK_SELL"
        return "NEUTRAL"

    @staticmethod
    def _direction_from_score(score: Optional[float]) -> str:
        if score is None:
            return "UNKNOWN"
        if score > 0:
            return "BULLISH"
        if score < 0:
            return "BEARISH"
        return "NEUTRAL"

    def _to_evidence(self, result: TimeframeResult) -> TimeframeEvidence:
        """Convert a TimeframeResult to TimeframeEvidence."""
        score = self._safe_float(result.score)
        status = result.status.upper()
        fallback_depth = result.fallback_depth
        confidence_multiplier = self._safe_float(result.confidence_multiplier)
        if confidence_multiplier is None:
            confidence_multiplier = (
                1.0 if status == "VALID"
                else 0.55 if fallback_depth == 1
                else 0.55 ** fallback_depth if fallback_depth > 0
                else 0.0
            )
        data_quality_score = self._safe_float(result.data_quality_score)
        if data_quality_score is None:
            data_quality_score = confidence_multiplier * 100.0

        return TimeframeEvidence(
            requested_timeframe=result.requested_timeframe,
            source_timeframe=result.used_timeframe,
            score=score,
            data_status=status,
            fallback_depth=fallback_depth,
            confidence_multiplier=self._clamp(confidence_multiplier),
            data_quality_score=max(0.0, min(100.0, data_quality_score)),
            bars_available=result.bars_available,
            bars_required=result.bars_required,
        )

    # Strategic, Swing, Tactical weights (from config or hardcoded)
    STRATEGIC_WEIGHTS = {"MN1": 0.20, "W1": 0.35, "D1": 0.45}
    SWING_WEIGHTS = {"D1": 0.55, "H4": 0.45}
    TACTICAL_WEIGHTS = {"H4": 0.25, "H1": 0.35, "M30": 0.25, "M15": 0.15}
    OVERALL_WEIGHTS = {"STRATEGIC": 0.45, "SWING": 0.35, "TACTICAL": 0.20}

    def _deduplicate_source_evidence(
        self,
        evidence: Dict[str, TimeframeEvidence],
        weights: Dict[str, float],
    ) -> List[Tuple[TimeframeEvidence, float]]:
        """
        Prevent fallback copies from being treated as independent observations.
        """
        grouped: Dict[str, List[Tuple[TimeframeEvidence, float]]] = {}
        for tf, weight in weights.items():
            item = evidence.get(tf)
            if item is None or not item.is_usable:
                continue
            source = item.source_key
            if source is None:
                continue
            grouped.setdefault(source, []).append((item, float(weight)))

        result: List[Tuple[TimeframeEvidence, float]] = []
        for source, members in grouped.items():
            # Pick the highest-quality representative
            representative = max(members, key=lambda x: (x[0].data_quality_score, -x[0].fallback_depth))[0]
            total_weight = sum(w for _, w in members)
            effective_weight = total_weight * representative.confidence_multiplier
            result.append((representative, effective_weight))
        return result

    def _calculate_weighted_score(
        self,
        evidence: Dict[str, TimeframeEvidence],
        weights: Dict[str, float],
    ) -> Dict[str, Any]:
        grouped = self._deduplicate_source_evidence(evidence, weights)
        if not grouped:
            return {
                "score": None,
                "data_quality_score": 0.0,
                "confidence_multiplier": 0.0,
                "confidence_rating": "NONE",
                "alignment_rating": "NO_DATA",
                "direction": "UNKNOWN",
                "rating": "NO_DATA",
                "effective_weight": 0.0,
                "source_count": 0,
            }

        weighted_sum = 0.0
        effective_weight = 0.0
        quality_sum = 0.0
        quality_weight = 0.0
        scores = []

        for item, w in grouped:
            if item.score is None:
                continue
            weighted_sum += item.score * w
            effective_weight += w
            quality_sum += item.data_quality_score * w
            quality_weight += w
            scores.append(item.score)

        if effective_weight <= 0:
            return {
                "score": None,
                "data_quality_score": 0.0,
                "confidence_multiplier": 0.0,
                "confidence_rating": "NONE",
                "alignment_rating": "NO_DATA",
                "direction": "UNKNOWN",
                "rating": "NO_DATA",
                "effective_weight": 0.0,
                "source_count": 0,
            }

        score = weighted_sum / effective_weight
        data_quality = quality_sum / quality_weight if quality_weight > 0 else 0.0

        # Alignment
        positive = sum(1 for x in scores if x > 10)
        negative = sum(1 for x in scores if x < -10)
        total = len(scores)
        if total == 0:
            alignment = "NO_DATA"
        elif positive == total or negative == total:
            alignment = "STRONG_ALIGNMENT"
        elif positive >= math.ceil(total * 0.67) or negative >= math.ceil(total * 0.67):
            alignment = "MODERATE_ALIGNMENT"
        else:
            alignment = "MIXED"

        # Source independence
        requested_count = sum(1 for tf in weights if tf in evidence and evidence[tf].is_usable)
        if requested_count <= 0:
            independence_factor = 0.0
        else:
            independence_factor = min(1.0, len(grouped) / requested_count)

        alignment_factor = {"STRONG_ALIGNMENT": 1.0, "MODERATE_ALIGNMENT": 0.85, "MIXED": 0.65, "NO_DATA": 0.0}.get(
            alignment, 0.0
        )

        quality_factor = data_quality / 100.0
        confidence_multiplier = self._clamp(
            quality_factor * alignment_factor * (0.75 + 0.25 * independence_factor)
        )
        confidence_percent = confidence_multiplier * 100.0
        if confidence_percent >= 80:
            confidence_rating = "HIGH"
        elif confidence_percent >= 60:
            confidence_rating = "MEDIUM"
        elif confidence_percent >= 35:
            confidence_rating = "LOW"
        else:
            confidence_rating = "VERY_LOW"

        return {
            "score": round(score, 6),
            "data_quality_score": round(data_quality, 4),
            "confidence_multiplier": round(confidence_multiplier, 4),
            "confidence_rating": confidence_rating,
            "alignment_rating": alignment,
            "direction": self._direction_from_score(score),
            "rating": self._rating_from_score(score),
            "effective_weight": round(effective_weight, 6),
            "source_count": len(grouped),
            "independence_factor": round(independence_factor, 4),
        }

    def _overall_alignment(
        self,
        strategic: Dict[str, Any],
        swing: Dict[str, Any],
        tactical: Dict[str, Any],
    ) -> str:
        values = [strategic.get("score"), swing.get("score"), tactical.get("score")]
        values = [v for v in values if v is not None]
        if not values:
            return "NO_DATA"
        bullish = sum(1 for v in values if v > 10)
        bearish = sum(1 for v in values if v < -10)
        if bullish == len(values) or bearish == len(values):
            return "STRONG_ALIGNMENT"
        if bullish >= 2 or bearish >= 2:
            return "MODERATE_ALIGNMENT"
        return "MIXED"

    def _calculate_multi_timeframe_intelligence(
        self,
        results_by_timeframe: Dict[str, TimeframeResult],
    ) -> Dict[str, Dict[str, Any]]:
        evidence = {tf: self._to_evidence(res) for tf, res in results_by_timeframe.items() if res is not None}

        strategic = self._calculate_weighted_score(evidence, self.STRATEGIC_WEIGHTS)
        swing = self._calculate_weighted_score(evidence, self.SWING_WEIGHTS)
        tactical = self._calculate_weighted_score(evidence, self.TACTICAL_WEIGHTS)

        # Overall
        components = {"STRATEGIC": strategic, "SWING": swing, "TACTICAL": tactical}
        weighted_sum = 0.0
        total_weight = 0.0
        quality_sum = 0.0
        confidence_sum = 0.0

        for name, weight in self.OVERALL_WEIGHTS.items():
            comp = components[name]
            score = comp.get("score")
            if score is None:
                continue
            weighted_sum += score * weight
            total_weight += weight
            quality_sum += comp["data_quality_score"] * weight
            confidence_sum += comp["confidence_multiplier"] * weight

        if total_weight <= 0:
            overall = {
                "score": None,
                "rating": "NO_DATA",
                "direction": "UNKNOWN",
                "data_quality_score": 0.0,
                "confidence_multiplier": 0.0,
                "confidence_rating": "NONE",
                "alignment_rating": "NO_DATA",
            }
        else:
            overall_score = weighted_sum / total_weight
            overall_quality = quality_sum / total_weight
            component_confidence = confidence_sum / total_weight
            overall = {
                "score": round(overall_score, 6),
                "rating": self._rating_from_score(overall_score),
                "direction": self._direction_from_score(overall_score),
                "data_quality_score": round(overall_quality, 4),
                "confidence_multiplier": round(component_confidence, 4),
                "confidence_rating": (
                    "HIGH" if component_confidence >= 0.80 else
                    "MEDIUM" if component_confidence >= 0.60 else
                    "LOW" if component_confidence >= 0.35 else
                    "VERY_LOW"
                ),
                "alignment_rating": self._overall_alignment(strategic, swing, tactical),
            }

        return {"STRATEGIC": strategic, "SWING": swing, "TACTICAL": tactical, "OVERALL": overall}

    # ------------------------------------------------------------------
    # COMPOSITE STORAGE (REPLACED)
    # ------------------------------------------------------------------

    def compute_and_store_composites(self):
        for idx_name, results in self.all_results.items():
            intelligence = self._calculate_multi_timeframe_intelligence(results)
            for comp_name in ["STRATEGIC", "SWING", "TACTICAL", "OVERALL"]:
                comp = intelligence[comp_name]
                score = comp.get("score")
                if score is None:
                    continue
                rating = self._rating_from_score(score)
                data = {
                    "symbol": idx_name,
                    "timeframe": comp_name,
                    "index_value": None,
                    "normalized_value": None,
                    "return_1d": None,
                    "return_1w": None,
                    "return_1m": None,
                    "momentum": None,
                    "trend_score": None,
                    "volatility": None,
                    "rating": rating,
                    "overall_score": score,
                    "confidence": comp.get("confidence_multiplier", 0.7),
                    "data_quality": "COMPOSITE",
                    "data_status": "VALID",
                    "fallback_from": None,
                    "used_timeframe": None,
                    "bars_available": None,
                    "bars_required": None,
                    "fallback_depth": None,
                    "confidence_multiplier": comp.get("confidence_multiplier", 1.0),
                    "data_quality_score": comp.get("data_quality_score", 100.0),
                    "alignment_score": None,  # we don't store a numeric alignment score separately
                    "alignment_rating": comp.get("alignment_rating"),
                    "confidence_rating": comp.get("confidence_rating"),
                    "calculated_at": datetime.utcnow(),
                }
                self.repo.upsert_index_current(data)
                self.repo.insert_history(data)
                logger.info(f"{idx_name} {comp_name}: score={score:.2f}, rating={rating}")

    def run(self):
        self.connect()
        logger.info("Starting Currency Index Engine (Final: Institutional Aggregation)")

        indices = list(BASKETS.keys())
        timeframes = config.timeframe_config.keys()

        self.all_results = {}

        for idx_name, basket in BASKETS.items():
            pairs = basket['pairs']
            idx_results = {}
            for tf in timeframes:
                result = self.resolve_timeframe(idx_name, pairs, tf)
                idx_results[tf] = result
                self.store_timeframe_result(idx_name, tf, result)
                if result.score is not None:
                    logger.info(f"{idx_name} {tf}: score={result.score:.2f}, status={result.status}, used={result.used_timeframe}")
                else:
                    logger.info(f"{idx_name} {tf}: score=N/A, status={result.status}, used={result.used_timeframe}")

            self.all_results[idx_name] = idx_results

        self.compute_and_store_composites()
        self.conn.close()
        logger.info("Currency Index Engine finished")

    def store_timeframe_result(self, idx_name, requested_tf, result: TimeframeResult):
        rating = compute_rating(result.score) if result.score is not None else 'NO_DATA'
        conf = (result.data_quality_score / 100.0) * 0.8 + 0.2
        data = {
            'symbol': idx_name,
            'timeframe': requested_tf,
            'index_value': None,
            'normalized_value': None,
            'return_1d': None,
            'return_1w': None,
            'return_1m': None,
            'momentum': None,
            'trend_score': None,
            'volatility': None,
            'rating': rating,
            'overall_score': result.score,
            'confidence': conf,
            'data_quality': result.status,
            'data_status': result.status,
            'fallback_from': requested_tf if result.status == 'FALLBACK' else None,
            'used_timeframe': result.used_timeframe,
            'bars_available': result.bars_available,
            'bars_required': result.bars_required,
            'fallback_depth': result.fallback_depth,
            'confidence_multiplier': result.confidence_multiplier,
            'data_quality_score': result.data_quality_score,
            'alignment_score': None,
            'alignment_rating': None,
            'confidence_rating': None,
            'calculated_at': datetime.utcnow(),
        }
        self.repo.upsert_index_current(data)
        self.repo.insert_history(data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = CurrencyIndexEngine()
    engine.run()
