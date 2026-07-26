import logging
import os

import pandas as pd

from intelligence.data.common.writer import DataWriter
from intelligence.data.historical.normalization.ohlc_normalizer import normalize_ohlc
from intelligence.data.historical.validation.ohlc_validator import validate_ohlc

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_landing_zone():
    landing_dir = "data/landing/historical"
    if not os.path.exists(landing_dir):
        logger.error(f"Landing directory not found: {landing_dir}")
        return

    files = os.listdir(landing_dir)
    # Group by symbol/timeframe
    groups = {}
    for f in files:
        if not f.endswith(".csv"):
            continue
        parts = f.split("_")
        if len(parts) < 3:
            continue
        symbol = parts[0]
        timeframe = parts[1]
        key = f"{symbol}_{timeframe}"
        groups.setdefault(key, []).append(f)

    logger.info(
        f"Found {len(groups)} symbol/timeframe groups, {len(files)} total files."
    )

    writer = DataWriter()
    total_inserted = 0

    for key, file_list in groups.items():
        symbol, timeframe = key.split("_")
        logger.info(f"Processing {symbol} {timeframe} ({len(file_list)} files)")
        all_dfs = []
        for f in file_list:
            filepath = os.path.join(landing_dir, f)
            try:
                df = pd.read_csv(filepath, parse_dates=["time"])
                all_dfs.append(df)
            except Exception as e:
                logger.warning(f"Could not read {f}: {e}")
        if not all_dfs:
            logger.warning(f"No data for {symbol} {timeframe}")
            continue
        combined = pd.concat(all_dfs, ignore_index=True)
        combined.drop_duplicates(subset=["time"], inplace=True)
        norm = normalize_ohlc(combined, symbol, timeframe, "dukascopy")
        valid, invalid, issues = validate_ohlc(norm)
        if invalid > 0:
            logger.warning(f"Validation issues: {issues}")
        if valid.empty:
            logger.warning(f"No valid data for {symbol} {timeframe}")
            continue
        records = valid.to_dict("records")
        inserted = writer.write_ohlcv(records)
        total_inserted += inserted
        logger.info(f"Inserted {inserted} rows for {symbol} {timeframe}")

    logger.info(f"Total inserted: {total_inserted}")


if __name__ == "__main__":
    process_landing_zone()
