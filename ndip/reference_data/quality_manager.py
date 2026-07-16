class QualityManager:
    PROVIDER_RANKS = {
        "yahoo_metadata": 5,
        "mt5_metadata": 10,
        "polygon_metadata": 8,
        "alpha_vantage_metadata": 6,
    }

    def score(self, metadata: dict, provider: str) -> float:
        base_score = 1.0
        for field in ["symbol", "asset_class", "exchange_code", "base_currency"]:
            if not metadata.get(field):
                base_score -= 0.2
        rank = self.PROVIDER_RANKS.get(provider, 5)
        boost = rank / 10.0
        return max(0.0, min(1.0, base_score * (0.8 + 0.2 * boost)))

    def get_provider_rank(self, provider: str) -> int:
        return self.PROVIDER_RANKS.get(provider, 5)
