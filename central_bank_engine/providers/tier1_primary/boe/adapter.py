from datetime import datetime
from typing import Any, Dict

from central_bank_engine.dtos import UniversalCentralBankEvent


class BOEAdapter:
    def adapt(self, raw: Dict[str, Any], provider_name: str) -> UniversalCentralBankEvent:
        release_time = raw.get("release_time") or raw.get("effective_date") or datetime.now().isoformat()
        if isinstance(release_time, str):
            release_time = datetime.fromisoformat(release_time.replace("Z", "+00:00"))

        rate = raw.get("rate")
        old_rate = raw.get("old_rate")
        rate_change = None
        if rate and old_rate:
            rate_change = rate - old_rate

        return UniversalCentralBankEvent(
            event_id=raw.get("event_id", "boe_" + release_time.isoformat()),
            provider=provider_name,
            bank=raw.get("bank", "Bank of England"),
            country=raw.get("country", "UK"),
            currency=raw.get("currency", "GBP"),
            event_type=raw.get("event_type", "RateDecision"),
            title=raw.get("title", "Bank of England Rate Decision"),
            summary=raw.get("summary", ""),
            statement=raw.get("statement", ""),
            release_time=release_time,
            meeting_date=raw.get("meeting_date"),
            effective_date=raw.get("effective_date"),
            old_rate=old_rate,
            new_rate=rate,
            rate_change=rate_change,
            vote_split=raw.get("vote_split"),
            governor=raw.get("governor", "Andrew Bailey"),
            importance=raw.get("importance", "High"),
            policy_bias=raw.get("policy_bias"),
            communication_type=raw.get("communication_type", "Statement"),
            source_url=raw.get("source_url"),
            attachments=raw.get("attachments", []),
            confidence=0.95,
            metadata=raw.get("metadata", {}),
        )
