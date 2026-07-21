# -*- coding: utf-8 -*-
"""API gateway for ECO-002"""


class EarningsGateway:
    def get_earnings(self, symbol):
        return {"symbol": symbol, "earnings": []}

    def get_financial_statements(self, symbol):
        return {"symbol": symbol, "statements": []}
