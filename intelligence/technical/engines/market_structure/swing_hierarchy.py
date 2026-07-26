"""
Classify swings by importance based on timeframe.
"""

from typing import List, Dict
from intelligence.technical.engines.market_structure.engine import SwingPoint

HIERARCHY_MAP = {
    'D1': 'major',
    'H4': 'intermediate',
    'H1': 'minor',
    'M15': 'micro',
    'M5': 'micro',
}

def classify_swings(swings: List[SwingPoint], timeframe: str) -> List[Dict]:
    level = HIERARCHY_MAP.get(timeframe, 'minor')
    result = []
    for s in swings:
        result.append({
            'time': s.time,
            'price': s.price,
            'type': s.type,
            'strength': s.strength,
            'hierarchy': level
        })
    return result
