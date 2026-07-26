from pathlib import Path

import yaml

from macroeconomic_events_engine.dtos import UniversalMacroEvent


class MacroClassifier:
    def __init__(self, ontology_path: str = None):
        if ontology_path is None:
            ontology_path = Path(__file__).parent / "ontology.yaml"
        with open(ontology_path, "r") as f:
            self.ontology = yaml.safe_load(f)

    def classify(self, event: UniversalMacroEvent) -> UniversalMacroEvent:
        """Classify event into category and subcategory based on title."""
        title = event.title.lower()
        for category, keywords in self.ontology.items():
            for keyword in keywords:
                if keyword.lower() in title:
                    event.category = category
                    event.subcategory = keyword
                    break
            if event.category != "Unknown":
                break
        if event.category == "Unknown":
            event.category = "Other"
        return event

    def get_keywords(self) -> dict[str, list[str]]:
        return self.ontology
