"""Engine registry – registers all engine adapters."""

from runtime.base_engine import BaseRawEngine

# Import adapters only if they exist
try:
    from runtime.adapters.central_bank import CentralBankEngineAdapter
except ImportError:
    CentralBankEngineAdapter = None

try:
    from runtime.adapters.financial_news import FinancialNewsEngineAdapter
except ImportError:
    FinancialNewsEngineAdapter = None

try:
    from runtime.adapters.macro_events import MacroEventsEngineAdapter
except ImportError:
    MacroEventsEngineAdapter = None

try:
    from runtime.adapters.cot_engine import COTEngineAdapter
except ImportError:
    COTEngineAdapter = None


class EngineRegistry:
    def __init__(self):
        self.engines: list[BaseRawEngine] = []

    def register(self, engine: BaseRawEngine) -> None:
        self.engines.append(engine)

    def get_all(self) -> list[BaseRawEngine]:
        return self.engines

    def get_enabled(self) -> list[BaseRawEngine]:
        return [e for e in self.engines if e.enabled]


# Singleton
registry = EngineRegistry()


def register_engines():
    """Register all available engines."""
    if CentralBankEngineAdapter:
        registry.register(CentralBankEngineAdapter())
    if FinancialNewsEngineAdapter:
        registry.register(FinancialNewsEngineAdapter())
    if MacroEventsEngineAdapter:
        registry.register(MacroEventsEngineAdapter())
    if COTEngineAdapter:
        registry.register(COTEngineAdapter())
