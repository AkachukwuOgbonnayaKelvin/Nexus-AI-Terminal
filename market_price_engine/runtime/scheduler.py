# -*- coding: utf-8 -*-
"""MKT-001 Runtime Scheduler - Called by Central Scheduler"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def run_mkt001():
    """Run MKT-001 data acquisition"""
    print("[MKT-001] Running market price data acquisition...")
    
    try:
        from market_price_engine.acquisition.incremental_loader import IncrementalLoader
        loader = IncrementalLoader()
        
        # Get all symbols from initialization
        from market_price_engine.acquisition.initialization import HistoricalInitializer
        initializer = HistoricalInitializer()
        symbols = initializer.ALL_SYMBOLS
        
        print(f"[MKT-001] Updating {len(symbols)} symbols...")
        
        # Update each symbol (incremental update only)
        updated = 0
        for symbol in symbols:
            try:
                bars = loader.load_data(symbol, "D1", 90)
                if bars:
                    updated += 1
            except Exception as e:
                print(f"[MKT-001] Error updating {symbol}: {e}")
        
        print(f"[MKT-001] Market price data acquisition complete: {updated} symbols updated")
        return {"status": "SUCCESS", "symbols": len(symbols), "updated": updated}
        
    except Exception as e:
        print(f"[MKT-001] Error: {e}")
        return {"status": "FAILED", "error": str(e)}


def run_mkt001_full():
    """Run full historical backfill for MKT-001"""
    print("[MKT-001] Running full historical backfill...")
    
    try:
        from market_price_engine.acquisition.initialization import HistoricalInitializer
        initializer = HistoricalInitializer()
        results = initializer.initialize_90_days()
        
        print(f"[MKT-001] Historical backfill complete: {results['successful']} symbols")
        return {"status": "SUCCESS", "results": results}
        
    except Exception as e:
        print(f"[MKT-001] Error: {e}")
        return {"status": "FAILED", "error": str(e)}
