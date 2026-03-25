from dataclasses import dataclass
from Vehicle import Car, Motorcycle

@dataclass
class ElectricMixin:
    charge: int = 0

    @property
    def is_electric(self) -> bool:
        return True

@dataclass
class ElectricCar(ElectricMixin, Car):
    @property
    def vehicle_type(self) -> str:
        return "electric_car"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["charge"] = self.charge
        return data

@dataclass
class ElectricBike(ElectricMixin, Motorcycle):
    @property
    def vehicle_type(self) -> str:
        return "electric_bike"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["charge"] = self.charge
        return data

@dataclass
class AutonomousElectricCar(ElectricCar):
    software_version: str = "1.0"

    @property
    def vehicle_type(self) -> str:
        return "autonomous_electric_car"

    @property
    def is_autonomous(self) -> bool:
        return True

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["software_version"] = self.software_version
        return data
