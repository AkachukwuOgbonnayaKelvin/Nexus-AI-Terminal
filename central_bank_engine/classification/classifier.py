class CentralBankClassifier:
    def __init__(self):
        self.event_type_map = {
            "RateDecision": "Policy",
            "Minutes": "Policy",
            "PressConference": "Communication",
            "Speech": "Communication",
            "Statement": "Policy",
            "MeetingCalendar": "Schedule",
            "BalanceSheet": "Policy",
            "ForwardGuidance": "Policy",
        }

    def classify(self, event_type: str) -> dict:
        category = self.event_type_map.get(event_type, "Other")
        return {"category": category}
