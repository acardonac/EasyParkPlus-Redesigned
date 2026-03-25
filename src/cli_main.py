import argparse
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from models import ParkingSlot, ParkingLot
from events import EventBus
from services import ParkingService, SearchService, ValetService, CustomerService
from agent_layer import AgentGateway

def build_demo_lot():
    slots = [
        ParkingSlot(slot_id=1, level=1),
        ParkingSlot(slot_id=2, level=1),
        ParkingSlot(slot_id=3, level=1, supports_electric=True),
        ParkingSlot(slot_id=4, level=1, supports_electric=True, supports_autonomous=True),
        ParkingSlot(slot_id=5, level=1, supports_large_vehicle=False),
        ParkingSlot(slot_id=6, level=1, supports_electric=True, supports_large_vehicle=False),
    ]
    return ParkingLot(level=1, slots=slots)

def build_gateway():
    event_bus = EventBus()
    lot = build_demo_lot()
    parking_service = ParkingService(lot, event_bus)
    search_service = SearchService(lot)
    valet_service = ValetService(parking_service, event_bus)
    customer_service = CustomerService(search_service, parking_service)
    return AgentGateway(parking_service, valet_service, customer_service, event_bus)

def main():
    parser = argparse.ArgumentParser(description="Parking Lot Manager - CLI")
    parser.add_argument("action", help="park_vehicle, request_valet, get_customer_help, list_events")
    parser.add_argument("--params", default="{}", help="JSON string of parameters")
    args = parser.parse_args()

    gateway = build_gateway()
    params = json.loads(args.params)
    result = gateway.execute(args.action, params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
