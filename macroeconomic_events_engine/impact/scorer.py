from macroeconomic_events_engine.dtos import UniversalMacroEvent


class ImpactScorer:
    def __init__(self):
        self.asset_mapping = {
            "USD": ["USD", "Gold", "US10Y", "US500", "EURUSD", "USDJPY"],
            "EUR": ["EUR", "EURUSD", "EURGBP", "Bund", "GER40"],
            "GBP": ["GBP", "GBPUSD", "EURGBP", "Gilt", "UK100"],
            "JPY": ["JPY", "USDJPY", "EURJPY", "JGB", "JP225"],
            "CAD": ["CAD", "USDCAD", "Oil", "CA10Y"],
            "AUD": ["AUD", "AUDUSD", "AUDJPY", "AU200"],
            "NZD": ["NZD", "NZDUSD", "NZDJPY"],
            "CHF": ["CHF", "USDCHF", "EURCHF"],
            "Gold": ["Gold", "XAUUSD", "Silver", "Gold Miners"],
            "Oil": ["Oil", "WTI", "Brent", "Energy Stocks"],
        }
        self.impact_base = {
            "High": 80,
            "Medium": 50,
            "Low": 20,
        }

    def score(self, event: UniversalMacroEvent) -> UniversalMacroEvent:
        base = self.impact_base.get(event.importance, 50)
        # Adjust based on country and category
        if event.country in ["US", "CN", "EU"]:
            base += 10
        if event.category in ["Inflation", "GDP", "Central Bank"]:
            base += 10
        # Apply cap
        event.impact_score = min(100, base)
        event.affected_assets = self._get_affected_assets(event)
        return event

    def _get_affected_assets(self, event: UniversalMacroEvent) -> list[str]:
        currency = event.currency
        assets = self.asset_mapping.get(currency, [currency])
        if event.category == "Inflation":
            assets.extend(["Gold", "Bonds", "Treasuries"])
        if event.category == "GDP":
            assets.extend(["Equities", "Commodities"])
        return list(set(assets))
