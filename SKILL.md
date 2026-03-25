# Parking Lot Manager - Agent Manifest

## Tool: park_vehicle
Description: Park a supported vehicle in the first compatible available slot.
Inputs:
- vehicle_type
- regnum
- make
- model
- color

## Tool: request_valet
Description: Create a valet or VIP valet reservation and park the vehicle.
Inputs:
- customer_id
- priority
- vehicle_type
- regnum
- make
- model
- color

## Tool: get_customer_help
Description: Handle customer-service tasks.
Inputs:
- request_type
- regnum (optional for find_vehicle)

## Tool: list_events
Description: Return emitted application events.
Inputs:
- none
