"""
GLB-004 Economic Events Intelligence Engine - Event Normalizer
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .schemas import EconomicEventInput
from ..constants import EventCategory, EventImpact, EventStatus, EVENT_TAXONOMY

logger = logging.getLogger(__name__)


class EventNormalizer:
    """Normalize raw event data into canonical format"""
    
    def __init__(self):
        self._taxonomy = EVENT_TAXONOMY
    
    def normalize(self, raw_event: Dict[str, Any]) -> Optional[EconomicEventInput]:
        """
        Normalize a raw event into canonical EconomicEventInput.
        
        Args:
            raw_event: Raw event data from provider
            
        Returns:
            EconomicEventInput or None if invalid
        """
        try:
            # Extract event name
            event_name = self._extract_event_name(raw_event)
            if not event_name:
                return None
            
            # Get event taxonomy
            taxonomy = self._get_taxonomy(event_name)
            if not taxonomy:
                # Unknown event - try to infer
                taxonomy = self._infer_taxonomy(raw_event)
                if not taxonomy:
                    # Default taxonomy
                    taxonomy = {
                        "currency": raw_event.get("currency", "USD"),
                        "category": EventCategory.GROWTH
                    }
            
            # Build canonical event
            return EconomicEventInput(
                event_id=raw_event.get("id", f"evt_{datetime.utcnow().timestamp()}"),
                event_name=event_name,
                country=raw_event.get("country", "Unknown"),
                currency=taxonomy.get("currency", "USD"),
                scheduled_at=self._parse_date(raw_event.get("date", datetime.utcnow().isoformat())),
                impact_level=self._determine_impact(raw_event, taxonomy),
                category=taxonomy.get("category", EventCategory.GROWTH),
                previous=raw_event.get("previous"),
                forecast=raw_event.get("forecast"),
                actual=raw_event.get("actual"),
                unit=raw_event.get("unit"),
                revision=raw_event.get("revision"),
                source=raw_event.get("source", "unknown"),
                status=self._determine_status(raw_event)
            )
            
        except Exception as e:
            logger.error(f"Error normalizing event: {e}")
            return None
    
    def _extract_event_name(self, raw: Dict) -> Optional[str]:
        """Extract event name from raw data"""
        name = raw.get("event") or raw.get("name") or raw.get("title")
        if name:
            return name.strip()
        return None
    
    def _get_taxonomy(self, event_name: str) -> Optional[Dict]:
        """Get taxonomy for an event name"""
        for category, events in self._taxonomy.items():
            for name, taxonomy in events.items():
                if name.lower() in event_name.lower() or event_name.lower() in name.lower():
                    return taxonomy
        return None
    
    def _infer_taxonomy(self, raw: Dict) -> Optional[Dict]:
        """Infer taxonomy from raw data"""
        currency = raw.get("currency", "")
        if currency == "USD":
            return {"currency": "USD", "category": EventCategory.GROWTH}
        elif currency == "EUR":
            return {"currency": "EUR", "category": EventCategory.GROWTH}
        elif currency == "GBP":
            return {"currency": "GBP", "category": EventCategory.GROWTH}
        elif currency == "JPY":
            return {"currency": "JPY", "category": EventCategory.GROWTH}
        return {"currency": "USD", "category": EventCategory.GROWTH}
    
    def _determine_impact(self, raw: Dict, taxonomy: Dict) -> EventImpact:
        """Determine event impact level"""
        # Check raw impact
        if "impact" in raw:
            impact = raw["impact"].upper()
            if impact in ["CRITICAL", "HIGH"]:
                return EventImpact.HIGH
            elif impact == "MEDIUM":
                return EventImpact.MEDIUM
            elif impact == "LOW":
                return EventImpact.LOW
        
        # Use base importance from taxonomy
        base_importance = taxonomy.get("base_importance", 50)
        if base_importance >= 80:
            return EventImpact.HIGH
        elif base_importance >= 60:
            return EventImpact.MEDIUM
        else:
            return EventImpact.LOW
    
    def _determine_status(self, raw: Dict) -> EventStatus:
        """Determine event status"""
        if "actual" in raw and raw["actual"] is not None:
            return EventStatus.RELEASED
        elif "revision" in raw and raw["revision"] is not None:
            return EventStatus.REVISED
        return EventStatus.UPCOMING
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse date string to datetime"""
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return datetime.utcnow()
