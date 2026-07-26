from datetime import UTC, datetime, timedelta

import pandas as pd
import yfinance as yf

from intelligence.data.common.writer import DataWriter

SYMBOL_MAP = {
    "US500": "^GSPC",
    "US100": "^IXIC",
    "US30": "^DJI",
    "GER40": "^GDAXI",
    "UK100": "^FTSE",
    "FRA40": "^FCHI",
    "JP225": "^N225",
    "HK50": "^HSI",
    "AU200": "^AXJO",
    "CL=F": "CL=F",
    "BZ=F": "BZ=F",
    "NG=F": "NG=F",
    "BTCUSD": "BTC-USD",
    "ETHUSD": "ETH-USD",
    "SOLUSD": "SOL-USD",
    "ADAUSD": "ADA-USD",
    "DOTUSD": "DOT-USD",
    "LINKUSD": "LINK-USD",
}


def fetch_yahoo(symbol, yf_symbol, start, end):
    ticker = yf.Ticker(yf_symbol)
    df = ticker.history(start=start, end=end, interval="1d")
    if df.empty:
        return pd.DataFrame()
    df.reset_index(inplace=True)
    # Find the date column
    date_col = None
    for col in df.columns:
        if col.lower() in ["date", "datetime", "time", "index"]:
            date_col = col
            break
    if date_col is None:
        date_col = df.columns[0]
    df.rename(columns={date_col: "time"}, inplace=True)
    df["time"] = pd.to_datetime(df["time"]).dt.tz_convert("UTC")
    # Rename OHLCV columns
    rename_map = {}
    for col in df.columns:
        lower = col.lower()
        if lower in ["open", "o"]:
            rename_map[col] = "open"
        elif lower in ["high", "h"]:
            rename_map[col] = "high"
        elif lower in ["low", "l"]:
            rename_map[col] = "low"
        elif lower in ["close", "c"]:
            rename_map[col] = "close"
        elif lower in ["volume", "vol"]:
            rename_map[col] = "volume"
    if rename_map:
        df.rename(columns=rename_map, inplace=True)
    # Ensure all needed columns exist
    needed = ["time", "open", "high", "low", "close", "volume"]
    for col in needed:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col} in data from {yf_symbol}")
    df["symbol"] = symbol
    df["timeframe"] = "D1"
    df["source"] = "yahoo_finance"
    df["quality_score"] = 0.9
    return df[needed + ["symbol", "timeframe", "source", "quality_score"]]


def main():
    writer = DataWriter()
    end = datetime.now(UTC)
    start = end - timedelta(days=5 * 365)
    for symbol, yf_symbol in SYMBOL_MAP.items():
        print(f"Fetching {symbol} ({yf_symbol})...")
        df = fetch_yahoo(symbol, yf_symbol, start, end)
        if df.empty:
            print(f"  No data for {symbol}")
            continue
        records = df.to_dict("records")
        inserted = writer.write_ohlcv(records)
        print(f"  Inserted {inserted} rows for {symbol}")


if __name__ == "__main__":
    main()
