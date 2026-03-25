# Architecture Summary

## Layers
- Presentation Layer: Tkinter UI and CLI
- Agent Enablement Layer: AgentGateway + tool schemas + policy engine
- Application Services: ParkingService, SearchService, ValetService, CustomerService
- Domain Model: Vehicle, ElectricVehicle, ParkingSlot, ParkingLot, Reservation, ParkingSession
- Event Layer: EventBus

## Why this is extensible
New vehicle types require:
1. A new class
2. A new registration in `VehicleFactory`

No changes are required in `ParkingLot` or the UI.

## Why this is AI-friendly
- Structured responses
- Event history
- Tool schemas
- Standardized actions
- Service-oriented orchestration
