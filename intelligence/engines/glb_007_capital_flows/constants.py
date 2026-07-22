"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Constants
"""

from enum import Enum


class CapitalFlowType(str, Enum):
    """Types of capital flows"""

    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    SAFE_HAVEN = "SAFE_HAVEN"
    EQUITY_ROTATION = "EQUITY_ROTATION"
    BOND_ROTATION = "BOND_ROTATION"
    CURRENCY_ROTATION = "CURRENCY_ROTATION"
    COMMODITY_FLOW = "COMMODITY_FLOW"
    LIQUIDITY_EXPANSION = "LIQUIDITY_EXPANSION"
    LIQUIDITY_CONTRACTION = "LIQUIDITY_CONTRACTION"
    FUNDING_STRESS = "FUNDING_STRESS"


class LiquidityState(str, Enum):
    """Liquidity states"""

    ABUNDANT = "ABUNDANT"
    NORMAL = "NORMAL"
    TIGHTENING = "TIGHTENING"
    STRESSED = "STRESSED"


class FlowDirection(str, Enum):
    """Flow direction"""

    INFLOW = "INFLOW"
    OUTFLOW = "OUTFLOW"
    NEUTRAL = "NEUTRAL"


class FlowMomentum(str, Enum):
    """Flow momentum"""

    ACCELERATING = "ACCELERATING"
    DECELERATING = "DECELERATING"
    STABLE = "STABLE"
    REVERSING = "REVERSING"


# NDIP Topics
NDIP_TOPICS = {
    "CAPITAL_FLOWS": "capital.flows",
    "ETF_FLOWS": "capital.etf_flows",
    "BOND_FLOWS": "capital.bond_flows",
    "EQUITY_FLOWS": "capital.equity_flows",
    "CURRENCY_FLOWS": "capital.currency_flows",
    "GLOBAL_LIQUIDITY": "liquidity.global",
    "FUNDING_CONDITIONS": "liquidity.funding",
    "CREDIT_CONDITIONS": "liquidity.credit",
}

# Asset exposure to capital flows
ASSET_FLOW_EXPOSURE = {
    # Safe havens (positive during risk-off)
    "XAUUSD": {"risk_off": 0.95, "safe_haven": 0.95},
    "USDCHF": {"risk_off": 0.85, "safe_haven": 0.85},
    "USDJPY": {"risk_off": 0.80, "safe_haven": 0.80},
    # Risk currencies (positive during risk-on)
    "AUDUSD": {"risk_on": 0.80, "commodity": 0.70},
    "NZDUSD": {"risk_on": 0.75, "commodity": 0.65},
    "USDCAD": {"risk_on": -0.60, "commodity": 0.65},
    "EURUSD": {"risk_on": 0.50, "risk_off": -0.50},
    "GBPUSD": {"risk_on": 0.45, "risk_off": -0.45},
    # Commodities
    "WTI": {"commodity": 0.85, "risk_on": 0.60},
    "BRENT": {"commodity": 0.85, "risk_on": 0.60},
    "XAGUSD": {"risk_on": 0.50, "safe_haven": 0.50},
    # Equities
    "US500": {"risk_on": 0.85, "risk_off": -0.85},
    "US100": {"risk_on": 0.90, "risk_off": -0.90},
    "US30": {"risk_on": 0.80, "risk_off": -0.80},
    "GER40": {"risk_on": 0.80, "risk_off": -0.80},
    "UK100": {"risk_on": 0.75, "risk_off": -0.75, "commodity": 0.40},
    "JP225": {"risk_on": 0.70, "risk_off": -0.70},
}
