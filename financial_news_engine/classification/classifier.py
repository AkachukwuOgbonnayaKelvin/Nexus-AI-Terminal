from typing import Dict


class NewsClassifier:
    def __init__(self):
        self.category_keywords = {
            "Central Bank": [
                "fed",
                "federal reserve",
                "ecb",
                "boe",
                "boj",
                "rates",
                "monetary",
                "policy",
            ],
            "Inflation": ["cpi", "inflation", "price", "ppi", "pce"],
            "Employment": ["nfp", "employment", "unemployment", "jobs", "claims"],
            "GDP": ["gdp", "growth", "economy", "recession"],
            "Commodities": ["oil", "gold", "silver", "copper", "wti", "brent"],
            "Forex": ["currency", "forex", "usd", "eur", "gbp", "jpy"],
            "Equities": ["stocks", "equities", "index", "sp500", "nasdaq", "dow"],
            "Bonds": ["yield", "treasury", "bond", "10y", "2y"],
            "Politics": ["election", "government", "congress", "senate", "president"],
            "Corporate": ["earnings", "revenue", "profit", "merger", "acquisition"],
        }
        self.importance_keywords = {
            "Critical": ["emergency", "urgent", "breaking"],
            "High": ["announces", "expects", "forecast", "update"],
        }

    def classify(self, headline: str, summary: str = "") -> Dict[str, str]:
        # Ensure summary is a string
        if summary is None:
            summary = ""
        text = (headline + " " + summary).lower()
        category = "General"
        for cat, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    category = cat
                    break
            if category != "General":
                break

        importance = "Low"
        text_lower = text.lower()
        for imp, keywords in self.importance_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    importance = imp
                    break
            if importance != "Low":
                break

        if category in ["Central Bank", "Inflation", "GDP", "Employment"]:
            if importance == "Low":
                importance = "High"
            elif importance == "High":
                importance = "Critical"

        return {"category": category, "importance": importance}
