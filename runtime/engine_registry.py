"""Engine registry – registers all engine adapters."""

from typing import List

from runtime.adapters.central_bank import CentralBankEngineAdapter
from runtime.adapters.financial_news import FinancialNewsEngineAdapter
from runtime.adapters.macro_events import MacroEventsEngineAdapter
from runtime.base_engine import BaseRawEngine


class EngineRegistry:
    def __init__(self):
        self.engines: List[BaseRawEngine] = []

    def register(self, engine: BaseRawEngine) -> None:
        self.engines.append(engine)

    def get_all(self) -> List[BaseRawEngine]:
        return self.engines

    def get_enabled(self) -> List[BaseRawEngine]:
        return [e for e in self.engines if e.enabled]


# Singleton
registry = EngineRegistry()


def register_engines():
    """Register all engines."""
    registry.register(CentralBankEngineAdapter())
    registry.register(FinancialNewsEngineAdapter())
    registry.register(MacroEventsEngineAdapter())
    # Add more engines here as adapters are created
