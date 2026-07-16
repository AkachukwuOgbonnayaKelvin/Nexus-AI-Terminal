class DependencyManager:
    def __init__(self):
        self._order = [
            "exchange",
            "currency",
            "country",
            "sector",
            "industry",
            "company",
            "asset_type",
        ]
        self._column_map = {
            "exchange": "exchange_code",
            "currency": "base_currency",
            "country": "country_code",
            "sector": "sector_id",
            "industry": "industry_id",
            "company": "company_id",
            "asset_type": "asset_type_id",
        }

    def get_order(self):
        return self._order

    def get_column(self, ref_type: str) -> str:
        return self._column_map.get(ref_type, ref_type)
