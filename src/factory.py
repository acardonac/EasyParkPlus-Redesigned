from Vehicle import Car, Motorcycle, Truck, Bus, AutonomousCar
from ElectricVehicle import ElectricCar, ElectricBike, AutonomousElectricCar

class VehicleFactory:
    _registry = {
        "car": Car,
        "motorcycle": Motorcycle,
        "truck": Truck,
        "bus": Bus,
        "electric_car": ElectricCar,
        "electric_bike": ElectricBike,
        "autonomous_car": AutonomousCar,
        "autonomous_electric_car": AutonomousElectricCar,
    }

    @classmethod
    def register(cls, vehicle_type: str, vehicle_class):
        cls._registry[vehicle_type] = vehicle_class

    @classmethod
    def supported_types(cls):
        return sorted(cls._registry.keys())

    @classmethod
    def create_vehicle(cls, vehicle_type: str, **kwargs):
        if vehicle_type not in cls._registry:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type}")
        return cls._registry[vehicle_type](**kwargs)
