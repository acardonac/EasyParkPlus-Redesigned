from dataclasses import dataclass, field
from typing import Optional, List
import uuid

@dataclass
class ParkingSlot:
    slot_id: int
    level: int
    supports_electric: bool = False
    supports_autonomous: bool = False
    supports_large_vehicle: bool = True
    vehicle: Optional[object] = None

    def is_empty(self) -> bool:
        return self.vehicle is None

    def can_accept(self, vehicle) -> bool:
        if not self.is_empty():
            return False
        if getattr(vehicle, "is_electric", False) and not self.supports_electric:
            return False
        if getattr(vehicle, "is_autonomous", False) and not self.supports_autonomous:
            return False
        if vehicle.vehicle_type in {"truck", "bus"} and not self.supports_large_vehicle:
            return False
        return True

    def park(self, vehicle):
        if not self.can_accept(vehicle):
            raise ValueError(f"Slot {self.slot_id} cannot accept {vehicle.vehicle_type}")
        self.vehicle = vehicle

    def remove_vehicle(self):
        self.vehicle = None

    def to_dict(self) -> dict:
        return {
            "slot_id": self.slot_id,
            "level": self.level,
            "supports_electric": self.supports_electric,
            "supports_autonomous": self.supports_autonomous,
            "supports_large_vehicle": self.supports_large_vehicle,
            "occupied": self.vehicle is not None,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None,
        }

@dataclass
class ParkingSession:
    vehicle_regnum: str
    slot_id: int
    session_id: str = field(default_factory=lambda: f"sess_{uuid.uuid4().hex[:8]}")
    status: str = "active"

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "vehicle_regnum": self.vehicle_regnum,
            "slot_id": self.slot_id,
            "status": self.status,
        }

@dataclass
class Reservation:
    customer_id: str
    vehicle_regnum: str
    service_type: str
    assigned_slot_id: Optional[int] = None
    reservation_id: str = field(default_factory=lambda: f"res_{uuid.uuid4().hex[:8]}")
    status: str = "confirmed"

    def to_dict(self) -> dict:
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "vehicle_regnum": self.vehicle_regnum,
            "service_type": self.service_type,
            "assigned_slot_id": self.assigned_slot_id,
            "status": self.status,
        }

class ParkingLot:
    def __init__(self, level: int, slots: List[ParkingSlot]):
        self.level = level
        self.slots = slots

    def get_slot(self, slot_id: int):
        for slot in self.slots:
            if slot.slot_id == slot_id:
                return slot
        return None

    def find_slot_for(self, vehicle):
        compatible_slots = [slot for slot in self.slots if slot.can_accept(vehicle)]
        compatible_slots.sort(key=lambda slot: slot.slot_id)
        return compatible_slots[0] if compatible_slots else None

    def park_vehicle(self, vehicle):
        slot = self.find_slot_for(vehicle)
        if slot is None:
            raise ValueError(f"No available compatible slot for {vehicle.vehicle_type}")
        slot.park(vehicle)
        return slot.slot_id

    def remove_vehicle(self, slot_id: int) -> bool:
        slot = self.get_slot(slot_id)
        if slot is None or slot.is_empty():
            return False
        slot.remove_vehicle()
        return True

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "slots": [slot.to_dict() for slot in self.slots],
        }
