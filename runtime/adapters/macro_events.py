import logging
import sys
from pathlib import Path

from runtime.base_engine import BaseRawEngine

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from macroeconomic_events_engine.acquisition import MacroCollector
from macroeconomic_events_engine.classification import MacroClassifier
from macroeconomic_events_engine.consensus import ConsensusResolver
from macroeconomic_events_engine.impact import ImpactScorer
from macroeconomic_events_engine.providers.tier1_primary.tradingeconomics import (
    TradingEconomicsAdapter,
    TradingEconomicsConnector,
)
from macroeconomic_events_engine.providers.tier2_secondary.forexfactory import (
    ForexFactoryAdapter,
    ForexFactoryConnector,
)
from macroeconomic_events_engine.providers.tier2_secondary.investing import (
    InvestingAdapter,
    InvestingConnector,
)
from macroeconomic_events_engine.warehouse import ConsensusWarehouse, RawWarehouse
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class MacroEventsEngineAdapter(BaseRawEngine):
    def __init__(self):
        self._initialized = False
        self.pm = None
        self.collector = None
        self.raw_warehouse = None
        self.consensus_warehouse = None
        self.classifier = None
        self.resolver = None
        self.scorer = None

    @property
    def name(self) -> str:
        return "macro_events"

    @property
    def enabled(self) -> bool:
        return True

    @property
    def interval_seconds(self) -> int:
        return 600

    async def initialize(self):
        if not self._initialized:
            logger.info("Initializing Macroeconomic Events Engine")
            self.pm = ProviderManager()
            te = TradingEconomicsConnector()
            te_adapter = TradingEconomicsAdapter()
            self.pm.register_provider(
                "trading_economics",
                te,
                te_adapter,
                capabilities=["macroeconomic_events"],
            )
            ff = ForexFactoryConnector()
            ff_adapter = ForexFactoryAdapter()
            self.pm.register_provider(
                "forexfactory", ff, ff_adapter, capabilities=["macroeconomic_events"]
            )
            inv = InvestingConnector()
            inv_adapter = InvestingAdapter()
            self.pm.register_provider(
                "investing", inv, inv_adapter, capabilities=["macroeconomic_events"]
            )
            self.collector = MacroCollector(self.pm)
            self.raw_warehouse = RawWarehouse()
            self.consensus_warehouse = ConsensusWarehouse()
            self.classifier = MacroClassifier()
            self.resolver = ConsensusResolver()
            self.scorer = ImpactScorer()
            self._initialized = True

    async def run(self):
        if not self._initialized:
            await self.initialize()
        logger.info("Running Macroeconomic Events Engine")
        events = await self.collector.collect_today()
        grouped = {}
        for ev in events:
            key = ev.title.split("(")[0].strip()
            grouped.setdefault(key, []).append(ev)
        stored = 0
        for key, evs in grouped.items():
            for ev in evs:
                ev = self.classifier.classify(ev)
                ev = self.scorer.score(ev)
                await self.raw_warehouse.store(ev, ev.provider)
            if len(evs) > 1:
                consensus_event = self.resolver.resolve(evs)
                if consensus_event:
                    await self.consensus_warehouse.store(consensus_event)
                    stored += 1
            else:
                await self.consensus_warehouse.store(evs[0])
                stored += 1
        return {"stored": stored, "collected": len(events)}

    async def shutdown(self):
        logger.info("Shutting down Macroeconomic Events Engine")
        self._initialized = False

    def health(self):
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "engine": "macro_events",
        }

    def metrics(self):
        return {"engine": "macro_events", "last_run": "N/A", "events": 0}
