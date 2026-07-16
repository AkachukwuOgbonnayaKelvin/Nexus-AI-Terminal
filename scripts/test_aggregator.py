#!/usr/bin/env python3
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio

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


async def main():
    print("=" * 60)
    print("TESTING CENTRAL BANK AGGREGATOR")
    print("=" * 60)

    # Mock events from collectors
    mock_events = [
        {
            "event_id": "fed_rate_1",
            "bank": "Federal Reserve",
            "country": "US",
            "currency": "USD",
            "event_type": "RATE_DECISION",
            "title": "Federal Funds Rate",
            "rate": 4.25,
            "release_time": "2026-07-30T14:00:00",
            "source": "FRED",
        },
        {
            "event_id": "fed_minutes_1",
            "bank": "Federal Reserve",
            "country": "US",
            "currency": "USD",
            "event_type": "MINUTES",
            "title": "FOMC Minutes",
            "release_time": "2026-08-21T14:00:00",
            "source": "RSS",
        },
        {
            "event_id": "ecb_rate_1",
            "bank": "European Central Bank",
            "country": "EU",
            "currency": "EUR",
            "event_type": "RATE_DECISION",
            "title": "ECB Interest Rate",
            "rate": 3.0,
            "release_time": "2026-07-24T12:00:00",
            "source": "placeholder",
        },
    ]

    # Pipeline stages
    router = CollectorRouter()
    validator = Validator()
    deduplicator = Deduplicator()
    normalizer = Normalizer()
    cycle_builder = PolicyCycleBuilder()
    linker = KnowledgeLinker()
    versioner = VersionManager()
    conf_engine = ConfidenceEngine()
    publisher = Publisher()

    print(f"\nStarting with {len(mock_events)} mock events")
    routed = router.route(mock_events)
    validated = validator.validate(routed)
    deduped = deduplicator.deduplicate(validated)
    normalized = normalizer.normalize(deduped)
    cycle_linked = cycle_builder.build([e.to_dict() for e in normalized])
    knowledge_linked = linker.link(cycle_linked)
    versioned = versioner.version(knowledge_linked)
    scored = conf_engine.score(versioned)

    print("\nProcessed events:")
    for ev in scored:
        print(
            f"  {ev.get('bank')} - {ev.get('event_type')}: {ev.get('title')} (cycle: {ev.get('policy_cycle_id')}, confidence: {ev.get('confidence'):.2f})"
        )
        if ev.get("affected_assets"):
            print(f"    Assets: {', '.join(ev.get('affected_assets', []))}")

    # Publish (dry-run)
    # We'll convert back to DTO for publishing
    from central_bank_engine.dtos import UniversalCentralBankEvent

    dtos = [UniversalCentralBankEvent(**ev) for ev in scored]
    print(f"\nPrepared {len(dtos)} events for publication.")
    # In production, call: await publisher.publish(dtos)

    print("\n✅ Aggregator test complete.")


if __name__ == "__main__":
    asyncio.run(main())
