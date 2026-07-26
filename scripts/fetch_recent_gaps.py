import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yfinance as yf
import psycopg2
import pandas as pd
from datetime import datetime, timedelta

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

# All symbols that need recent data
SYMBOLS = [
    'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'USDCHF', 'NZDUSD',
    'EURJPY', 'GBPJPY', 'AUDJPY', 'EURGBP', 'GBPAUD', 'GBPNZD', 'EURNZD',
    'AUDCAD', 'AUDNZD', 'EURCAD', 'EURCHF', 'GBPCAD', 'GBPCHF', 'NZDCAD', 'NZDJPY',
    'XAUUSD', 'XAGUSD', 'CL=F', 'BZ=F', 'NG=F', 'Copper', 'SpotBrent',
    'US500', 'US100', 'US30', 'GER40', 'UK100', 'FRA40', 'HK50', 'JP225',
    '^AXJO', '^IXIC', '^N225'
]

SYMBOL_MAP = {
    'EURUSD': 'EURUSD=X',
    'GBPUSD': 'GBPUSD=X',
    'USDJPY': 'USDJPY=X',
    'AUDUSD': 'AUDUSD=X',
    'USDCAD': 'USDCAD=X',
    'USDCHF': 'USDCHF=X',
    'NZDUSD': 'NZDUSD=X',
    'EURJPY': 'EURJPY=X',
    'GBPJPY': 'GBPJPY=X',
    'AUDJPY': 'AUDJPY=X',
    'EURGBP': 'EURGBP=X',
    'GBPAUD': 'GBPAUD=X',
    'GBPNZD': 'GBPNZD=X',
    'EURNZD': 'EURNZD=X',
    'AUDCAD': 'AUDCAD=X',
    'AUDNZD': 'AUDNZD=X',
    'EURCAD': 'EURCAD=X',
    'EURCHF': 'EURCHF=X',
    'GBPCAD': 'GBPCAD=X',
    'GBPCHF': 'GBPCHF=X',
    'NZDCAD': 'NZDCAD=X',
    'NZDJPY': 'NZDJPY=X',
    'XAUUSD': 'GC=F',
    'XAGUSD': 'SI=F',
    'CL=F': 'CL=F',
    'BZ=F': 'BZ=F',
    'NG=F': 'NG=F',
    'Copper': 'HG=F',
    'SpotBrent': 'BZ=F',
    'US500': '^GSPC',
    'US100': '^IXIC',
    'US30': '^DJI',
    'GER40': '^GDAXI',
    'UK100': '^FTSE',
    'FRA40': '^FCHI',
    'HK50': '^HSI',
    'JP225': '^N225',
    '^AXJO': '^AXJO',
    '^IXIC': '^IXIC',
    '^N225': '^N225',
}

def fetch_and_insert(symbol):
    yf_sym = SYMBOL_MAP.get(symbol)
    if not yf_sym:
        print(f"No mapping for {symbol}")
        return

    print(f"Fetching {symbol} ({yf_sym})...")
    try:
        ticker = yf.Ticker(yf_sym)
        df = ticker.history(period="7d", interval="1d")
        if df.empty:
            print(f"No recent data for {symbol}")
            return

        # Reset index to make date a column
        df = df.reset_index()

        # The date column is either 'Date' or 'Datetime'
        if 'Datetime' in df.columns:
            df = df.rename(columns={'Datetime': 'time'})
        elif 'Date' in df.columns:
            df = df.rename(columns={'Date': 'time'})
        else:
            # Fallback: assume first column is the date
            df = df.rename(columns={df.columns[0]: 'time'})

        df['symbol'] = symbol
        df['timeframe'] = 'D1'
        df['source'] = 'yahoo_finance'

        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
        })

        # Ensure time column is datetime
        df['time'] = pd.to_datetime(df['time'])

        conn = psycopg2.connect(DB_CONN)
        cur = conn.cursor()
        inserted = 0
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO raw.market_ohlcv
                    (time, symbol, timeframe, open, high, low, close, volume, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, timeframe, time) DO NOTHING
            """, (
                row['time'],
                row['symbol'],
                row['timeframe'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['volume'] if row['volume'] is not None else 0,
                'yahoo_finance'
            ))
            inserted += 1
        conn.commit()
        conn.close()
        print(f"Inserted {inserted} recent bars for {symbol}")
    except Exception as e:
        print(f"Error for {symbol}: {e}")

def main():
    for sym in SYMBOLS:
        fetch_and_insert(sym)

if __name__ == "__main__":
    main()
