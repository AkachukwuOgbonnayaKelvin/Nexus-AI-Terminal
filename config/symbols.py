"""Market symbols for Nexus AI Terminal."""

FOREX = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "NZDUSD",
    "USDCHF",
    "EURGBP",
    "EURJPY",
    "GBPJPY",
    "AUDJPY",
    "EURCHF",
    "USDCNH",
]

COMMODITIES = [
    "XAUUSD",
    "XAGUSD",
    "WTI",
    "BRENT",
    "NG",
    "COPPER",
    "PLATINUM",
    "PALLADIUM",
]

INDICES = [
    "US500",
    "US30",
    "US100",
    "GER40",
    "UK100",
    "FRA40",
    "JP225",
    "HK50",
    "AU200",
]

STOCKS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "NVDA",
    "META",
    "TSLA",
    "JPM",
    "V",
    "WMT",
    "JNJ",
    "PG",
    "UNH",
    "HD",
    "BAC",
    "XOM",
    "CVX",
    "KO",
    "PEP",
    "MCD",
]

CRYPTO = [
    "BTC-USD",
    "ETH-USD",
    "SOL-USD",
    "XRP-USD",
    "ADA-USD",
    "DOT-USD",
    "LINK-USD",
    "DOGE-USD",
    "SHIB-USD",
    "AVAX-USD",
    "MATIC-USD",
    "UNI-USD",
    "ATOM-USD",
]

ALL_SYMBOLS = FOREX + COMMODITIES + INDICES + STOCKS + CRYPTO

ASSET_CLASS_MAP = {
    "forex": FOREX,
    "commodity": COMMODITIES,
    "index": INDICES,
    "equity": STOCKS,
    "crypto": CRYPTO,
}
