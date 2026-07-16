class ConflictManager:
    ALIAS_MAP = {
        "exchange": {
            "NASDAQ": "NMS",
            "NYSE": "NYQ",
            "LSE": "LSE",
            "XETRA": "XET",
        },
        "currency": {},
    }

    def resolve(self, ref_type: str, value: str) -> str:
        if ref_type in self.ALIAS_MAP:
            alias_map = self.ALIAS_MAP[ref_type]
            return alias_map.get(value, value)
        return value
