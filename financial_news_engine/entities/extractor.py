import re
from typing import Dict, List


class EntityExtractor:
    def __init__(self):
        self.currency_patterns = re.compile(
            r"\b(USD|EUR|GBP|JPY|CHF|CAD|AUD|NZD|CNY|HKD)\b"
        )
        self.asset_patterns = re.compile(
            r"\b(Gold|Silver|Oil|WTI|Brent|Natural Gas|Copper)\b"
        )
        self.central_bank_patterns = re.compile(
            r"\b(Fed|Federal Reserve|ECB|BOE|BOJ|SNB|RBA|BOC)\b"
        )

    def extract(self, text: str) -> Dict[str, List[str]]:
        if not text:
            return {"currencies": [], "assets": [], "central_banks": []}
        return {
            "currencies": list(set(self.currency_patterns.findall(text))),
            "assets": list(set(self.asset_patterns.findall(text))),
            "central_banks": list(set(self.central_bank_patterns.findall(text))),
        }
