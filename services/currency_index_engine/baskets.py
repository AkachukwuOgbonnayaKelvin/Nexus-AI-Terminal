"""
Basket definitions for Nexus synthetic indices.
Each index is defined by a list of pair symbols and a formula type.
For geometric mean, we specify numerator and denominator pairs.
"""
from collections import OrderedDict

# Basket definitions: each index has a list of (symbol, role)
# role: 'num' for numerator, 'den' for denominator
# For geometric mean: index = (product(num) / product(den)) ^ (1 / count)
BASKETS = {
    'USDX': {
        'pairs': [
            ('USDCHF', 'num'),
            ('USDJPY', 'num'),
            ('EURUSD', 'den'),
            ('GBPUSD', 'den'),
        ],
        'description': 'Nexus equal-weight USD index'
    },
    'EURX': {
        'pairs': [
            ('EURUSD', 'num'),
            ('EURGBP', 'num'),
            ('EURJPY', 'num'),
            ('EURCHF', 'num'),
        ],
        'description': 'Nexus equal-weight EUR index'
    },
    'GBPX': {
        'pairs': [
            ('GBPUSD', 'num'),
            ('GBPJPY', 'num'),
            ('GBPCHF', 'num'),
            ('EURGBP', 'den'),   # invert because GBP is quote
        ],
        'description': 'Nexus equal-weight GBP index'
    },
    'JPYX': {
        'pairs': [
            ('USDJPY', 'den'),
            ('EURJPY', 'den'),
            ('GBPJPY', 'den'),
            ('CHFJPY', 'den'),
        ],
        'description': 'Nexus equal-weight JPY index (all den)'
    },
    'CHFX': {
        'pairs': [
            ('CHFJPY', 'num'),
            ('USDCHF', 'den'),
            ('EURCHF', 'den'),
            ('GBPCHF', 'den'),
        ],
        'description': 'Nexus equal-weight CHF index'
    },
    'AUDX': {
        'pairs': [
            ('AUDUSD', 'num'),
            ('AUDJPY', 'num'),
            ('AUDCAD', 'num'),
            ('AUDNZD', 'num'),
        ],
        'description': 'Nexus equal-weight AUD index'
    },
    'CADX': {
        'pairs': [
            ('CADJPY', 'num'),
            ('USDCAD', 'den'),
            ('EURCAD', 'den'),
            ('GBPCAD', 'den'),
        ],
        'description': 'Nexus equal-weight CAD index'
    },
    'NZDX': {
        'pairs': [
            ('NZDUSD', 'num'),
            ('NZDJPY', 'num'),
            ('NZDCAD', 'num'),
            ('AUDNZD', 'den'),   # invert because NZD is quote
        ],
        'description': 'Nexus equal-weight NZD index'
    },
}

# Official DXY weights (from ICE) for development/fallback
DXY_WEIGHTS = {
    'EURUSD': -0.576,
    'USDJPY': 0.136,
    'GBPUSD': -0.119,
    'USDCAD': 0.091,
    'USDSEK': 0.042,
    'USDCHF': 0.036,
}
DXY_CONSTANT = 50.14348112
