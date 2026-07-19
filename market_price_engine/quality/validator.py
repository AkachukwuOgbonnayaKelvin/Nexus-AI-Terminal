# -*- coding: utf-8 -*-
"""OHLCV Validator - Validates OHLCV data quality"""

from typing import Tuple, Optional
from providers.base import OHLCVData


class OHLCVValidator:
    """Validates OHLCV data quality"""
    
    def validate(self, bar: OHLCVData) -> Tuple[bool, Optional[str]]:
        """
        Validate an OHLCV bar.
        
        Returns:
            (is_valid, issue_message)
        """
        # Check for None values
        if bar.open is None or bar.high is None or bar.low is None or bar.close is None:
            return False, "Missing OHLC values"
        
        # Check for zero or negative prices
        if bar.open <= 0 or bar.high <= 0 or bar.low <= 0 or bar.close <= 0:
            return False, "Zero or negative price"
        
        # Check high >= low
        if bar.high < bar.low:
            return False, f"High ({bar.high}) < Low ({bar.low})"
        
        # Check high >= open and high >= close
        if bar.high < bar.open or bar.high < bar.close:
            return False, f"High ({bar.high}) < Open ({bar.open}) or Close ({bar.close})"
        
        # Check low <= open and low <= close
        if bar.low > bar.open or bar.low > bar.close:
            return False, f"Low ({bar.low}) > Open ({bar.open}) or Close ({bar.close})"
        
        # Check for valid timestamp
        if bar.timestamp is None:
            return False, "Missing timestamp"
        
        return True, None
