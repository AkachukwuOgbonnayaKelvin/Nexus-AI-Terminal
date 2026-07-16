from typing import Any, Dict


class CentralBankNormalizer:
    def normalize(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize field names and values."""
        # Set default policy_bias if not present
        if "policy_bias" not in record:
            record["policy_bias"] = "Unknown"
        # Set default communication_type
        if "communication_type" not in record:
            record["communication_type"] = "Statement"
        # Set default importance based on event_type
        if "importance" not in record:
            if record.get("event_type") in ["RateDecision", "Minutes"]:
                record["importance"] = "Critical"
            elif record.get("event_type") in ["Speech", "PressConference"]:
                record["importance"] = "High"
            else:
                record["importance"] = "Medium"
        return record
