"""Central Bank Engine – orchestrates collectors and aggregator."""

import logging
from typing import Any, Dict, List

from central_bank_engine.aggregator import (
    CollectorRouter,
    ConfidenceEngine,
    Deduplicator,
    KnowledgeLinker,
    Normalizer,
    PolicyCycleBuilder,
    Publisher,
    Validator,
    VersionManager,
)
from central_bank_engine.aggregator.publisher import Publisher as AggregatorPublisher
from central_bank_engine.collectors.boc import (
    BOCCalendarCollector,
    BOCMinutesCollector,
    BOCRateCollector,
    BOCSpeechCollector,
    BOCStatementCollector,
)
from central_bank_engine.collectors.boe import (
    BOECalendarCollector,
    BOEMinutesCollector,
    BOERateCollector,
    BOESpeechCollector,
    BOEStatementCollector,
)
from central_bank_engine.collectors.boj import (
    BOJCalendarCollector,
    BOJMinutesCollector,
    BOJRateCollector,
    BOJSpeechCollector,
    BOJStatementCollector,
)
from central_bank_engine.collectors.ecb import (
    ECBCalendarCollector,
    ECBMinutesCollector,
    ECBRateCollector,
    ECBSpeechCollector,
    ECBStatementCollector,
)
from central_bank_engine.collectors.federal_reserve import (
    FedCalendarCollector,
    FedMinutesCollector,
    FedRateCollector,
    FedSpeechCollector,
    FedStatementCollector,
)
from central_bank_engine.collectors.rba import (
    RBACalendarCollector,
    RBAMinutesCollector,
    RBARateCollector,
    RBASpeechCollector,
    RBAStatementCollector,
)
from central_bank_engine.collectors.rbnz import (
    RBNZCalendarCollector,
    RBNZMinutesCollector,
    RBNZRateCollector,
    RBNZSpeechCollector,
    RBNZStatementCollector,
)
from central_bank_engine.collectors.snb import (
    SNBCalendarCollector,
    SNBMinutesCollector,
    SNBRateCollector,
    SNBSpeechCollector,
    SNBStatementCollector,
)
from central_bank_engine.dtos import UniversalCentralBankEvent
from central_bank_engine.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class CentralBankEngine:
    def __init__(self):
        self.provider_manager = ProviderManager()
        self._register_collectors()

        # Aggregator pipeline stages
        self.router = CollectorRouter()
        self.validator = Validator()
        self.deduplicator = Deduplicator()
        self.normalizer = Normalizer()
        self.cycle_builder = PolicyCycleBuilder()
        self.linker = KnowledgeLinker()
        self.versioner = VersionManager()
        self.confidence = ConfidenceEngine()
        self.publisher = AggregatorPublisher()

    def _register_collectors(self):
        """Register all collectors for all banks."""
        # Federal Reserve
        self.provider_manager.register_collector(FedRateCollector())
        self.provider_manager.register_collector(FedSpeechCollector())
        self.provider_manager.register_collector(FedMinutesCollector())
        self.provider_manager.register_collector(FedStatementCollector())
        self.provider_manager.register_collector(FedCalendarCollector())

        # ECB
        self.provider_manager.register_collector(ECBRateCollector())
        self.provider_manager.register_collector(ECBSpeechCollector())
        self.provider_manager.register_collector(ECBMinutesCollector())
        self.provider_manager.register_collector(ECBStatementCollector())
        self.provider_manager.register_collector(ECBCalendarCollector())

        # BOE
        self.provider_manager.register_collector(BOERateCollector())
        self.provider_manager.register_collector(BOESpeechCollector())
        self.provider_manager.register_collector(BOEMinutesCollector())
        self.provider_manager.register_collector(BOEStatementCollector())
        self.provider_manager.register_collector(BOECalendarCollector())

        # BOJ
        self.provider_manager.register_collector(BOJRateCollector())
        self.provider_manager.register_collector(BOJSpeechCollector())
        self.provider_manager.register_collector(BOJMinutesCollector())
        self.provider_manager.register_collector(BOJStatementCollector())
        self.provider_manager.register_collector(BOJCalendarCollector())

        # SNB
        self.provider_manager.register_collector(SNBRateCollector())
        self.provider_manager.register_collector(SNBSpeechCollector())
        self.provider_manager.register_collector(SNBMinutesCollector())
        self.provider_manager.register_collector(SNBStatementCollector())
        self.provider_manager.register_collector(SNBCalendarCollector())

        # BOC
        self.provider_manager.register_collector(BOCRateCollector())
        self.provider_manager.register_collector(BOCSpeechCollector())
        self.provider_manager.register_collector(BOCMinutesCollector())
        self.provider_manager.register_collector(BOCStatementCollector())
        self.provider_manager.register_collector(BOCCalendarCollector())

        # RBA
        self.provider_manager.register_collector(RBARateCollector())
        self.provider_manager.register_collector(RBASpeechCollector())
        self.provider_manager.register_collector(RBAMinutesCollector())
        self.provider_manager.register_collector(RBAStatementCollector())
        self.provider_manager.register_collector(RBACalendarCollector())

        # RBNZ
        self.provider_manager.register_collector(RBNZRateCollector())
        self.provider_manager.register_collector(RBNZSpeechCollector())
        self.provider_manager.register_collector(RBNZMinutesCollector())
        self.provider_manager.register_collector(RBNZStatementCollector())
        self.provider_manager.register_collector(RBNZCalendarCollector())

        logger.info(f"Registered {len(self.provider_manager.collectors)} collectors")

    async def run(self) -> Dict[str, Any]:
        """Run the entire pipeline: collect → aggregate → publish."""
        logger.info("Starting Central Bank Intelligence Engine run")

        # Step 1: Collect raw events from all collectors
        raw_events = await self.provider_manager.run_all_collectors()
        logger.info(f"Collected {len(raw_events)} raw events")

        if not raw_events:
            return {"status": "success", "events": 0, "message": "No events collected"}

        # Step 2: Route, Validate, Deduplicate
        routed = self.router.route(raw_events)
        validated = self.validator.validate(routed)
        deduped = self.deduplicator.deduplicate(validated)

        # Step 3: Normalize to DTO
        normalized = self.normalizer.normalize(deduped)

        # Step 4: Build policy cycles
        # Convert DTOs back to dicts for pipeline stages (can be optimized)
        cycle_dicts = [e.to_dict() for e in normalized]
        cycle_linked = self.cycle_builder.build(cycle_dicts)

        # Step 5: Knowledge linking
        knowledge_linked = self.linker.link(cycle_linked)

        # Step 6: Version and confidence
        versioned = self.versioner.version(knowledge_linked)
        scored = self.confidence.score(versioned)

        # Step 7: Convert back to DTOs for publishing
        dtos = [UniversalCentralBankEvent(**ev) for ev in scored]

        # Step 8: Publish to NDIP
        publish_results = await self.publisher.publish(dtos)
        success_count = sum(1 for r in publish_results if r.get("success"))

        logger.info(f"Published {success_count} events to NDIP")

        return {
            "status": "success",
            "events": len(dtos),
            "published": success_count,
            "collector_status": self.provider_manager.get_collector_statuses(),
        }

    def get_status(self) -> Dict[str, Any]:
        """Get status of all collectors."""
        return {
            "collectors": self.provider_manager.get_collector_statuses(),
            "total_collectors": len(self.provider_manager.collectors),
        }
