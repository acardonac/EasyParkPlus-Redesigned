from dataclasses import dataclass, field
import uuid

@dataclass
class Vehicle:
    regnum: str
    make: str
    model: str
    color: str
    vehicle_id: str = field(default_factory=lambda: f"veh_{uuid.uuid4().hex[:8]}")

    @property
    def vehicle_type(self) -> str:
        return "vehicle"

    @property
    def is_electric(self) -> bool:
        return False

    @property
    def is_autonomous(self) -> bool:
        return False

    def to_dict(self) -> dict:
        return {
            "vehicle_id": self.vehicle_id,
            "regnum": self.regnum,
            "make": self.make,
            "model": self.model,
            "color": self.color,
            "vehicle_type": self.vehicle_type,
            "is_electric": self.is_electric,
            "is_autonomous": self.is_autonomous,
        }

@dataclass
class Car(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "car"

@dataclass
class Motorcycle(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "motorcycle"

@dataclass
class Truck(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "truck"

@dataclass
class Bus(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "bus"

@dataclass
class AutonomousCar(Car):
    software_version: str = "1.0"

    @property
    def vehicle_type(self) -> str:
        return "autonomous_car"

    @property
    def is_autonomous(self) -> bool:
        return True

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["software_version"] = self.software_version
        return data
