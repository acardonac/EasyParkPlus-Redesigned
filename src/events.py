from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class DomainEvent:
    event_type: str
    payload: dict
    timestamp: str

    @classmethod
    def create(cls, event_type: str, payload: dict):
        return cls(
            event_type=event_type,
            payload=payload,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }

class EventBus:
    def __init__(self):
        self._events = []

    def publish(self, event_type: str, payload: dict):
        event = DomainEvent.create(event_type, payload)
        self._events.append(event)
        return event

    def list_events(self):
        return [event.to_dict() for event in self._events]
