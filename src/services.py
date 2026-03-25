from factory import VehicleFactory
from models import ParkingSession, Reservation

def make_response(success: bool, message: str, data=None, error_code=None) -> dict:
    return {
        "success": success,
        "message": message,
        "error_code": error_code,
        "data": data,
    }

class ParkingService:
    def __init__(self, parking_lot, event_bus):
        self.parking_lot = parking_lot
        self.event_bus = event_bus
        self.sessions = {}

    def park_vehicle(self, vehicle_type: str, **vehicle_data):
        try:
            vehicle = VehicleFactory.create_vehicle(vehicle_type, **vehicle_data)
            slot_id = self.parking_lot.park_vehicle(vehicle)
            session = ParkingSession(vehicle_regnum=vehicle.regnum, slot_id=slot_id)
            self.sessions[session.session_id] = session
            self.event_bus.publish("vehicle_parked", {
                "slot_id": slot_id,
                "vehicle": vehicle.to_dict(),
                "session": session.to_dict(),
            })
            return make_response(
                True,
                "Vehicle parked successfully.",
                data={"slot_id": slot_id, "vehicle": vehicle.to_dict(), "session": session.to_dict()},
            )
        except ValueError as exc:
            return make_response(False, str(exc), error_code="PARKING_FAILED")

    def remove_vehicle(self, slot_id: int):
        removed = self.parking_lot.remove_vehicle(slot_id)
        if not removed:
            return make_response(False, f"Slot {slot_id} is empty or invalid.", error_code="REMOVE_FAILED")
        self.event_bus.publish("vehicle_removed", {"slot_id": slot_id})
        return make_response(True, "Vehicle removed successfully.", data={"slot_id": slot_id})

    def get_status(self):
        return make_response(True, "Retrieved parking lot status.", data=self.parking_lot.to_dict())

    def get_charge_status(self):
        evs = []
        for slot in self.parking_lot.slots:
            if slot.vehicle and getattr(slot.vehicle, "is_electric", False):
                evs.append({
                    "slot_id": slot.slot_id,
                    "regnum": slot.vehicle.regnum,
                    "charge": getattr(slot.vehicle, "charge", None),
                    "vehicle_type": slot.vehicle.vehicle_type,
                })
        return make_response(True, "Retrieved EV charge status.", data={"ev_vehicles": evs})

class SearchService:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

    def find_slot_by_regnum(self, regnum: str):
        for slot in self.parking_lot.slots:
            if slot.vehicle and slot.vehicle.regnum == regnum:
                return make_response(True, "Vehicle found.", data={"slot_id": slot.slot_id})
        return make_response(False, "Vehicle not found.", error_code="NOT_FOUND")

    def find_slots_by_color(self, color: str):
        slots = [slot.slot_id for slot in self.parking_lot.slots if slot.vehicle and slot.vehicle.color.lower() == color.lower()]
        return make_response(True, "Matching slots retrieved.", data={"slot_ids": slots})

    def find_regnums_by_color(self, color: str):
        regnums = [slot.vehicle.regnum for slot in self.parking_lot.slots if slot.vehicle and slot.vehicle.color.lower() == color.lower()]
        return make_response(True, "Matching registration numbers retrieved.", data={"regnums": regnums})

class ValetService:
    def __init__(self, parking_service, event_bus):
        self.parking_service = parking_service
        self.event_bus = event_bus
        self.reservations = {}

    def request_valet(self, customer_id: str, priority: str = "standard", **vehicle_data):
        result = self.parking_service.park_vehicle(**vehicle_data)
        if not result["success"]:
            return result

        slot_id = result["data"]["slot_id"]
        reservation = Reservation(
            customer_id=customer_id,
            vehicle_regnum=vehicle_data["regnum"],
            service_type="vip_valet" if priority == "vip" else "valet",
            assigned_slot_id=slot_id,
        )
        self.reservations[reservation.reservation_id] = reservation
        self.event_bus.publish("valet_assigned", {
            "customer_id": customer_id,
            "priority": priority,
            "reservation": reservation.to_dict(),
        })
        return make_response(
            True,
            "Valet request completed successfully.",
            data={"reservation": reservation.to_dict(), "parking": result["data"]},
        )

class CustomerService:
    def __init__(self, search_service, parking_service):
        self.search_service = search_service
        self.parking_service = parking_service

    def handle_request(self, request_type: str, **params):
        if request_type == "find_vehicle":
            return self.search_service.find_slot_by_regnum(params["regnum"])
        if request_type == "get_lot_status":
            return self.parking_service.get_status()
        if request_type == "get_ev_charge_status":
            return self.parking_service.get_charge_status()
        return make_response(False, f"Unsupported request type: {request_type}", error_code="UNKNOWN_REQUEST")
