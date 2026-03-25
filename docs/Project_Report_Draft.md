# Software Design & Architecture Project Report Draft

## 1. Overview
The original prototype mixed GUI code, domain logic, data storage, and output formatting inside a single module. The redesign separates responsibilities into a modular architecture with a domain layer, service layer, agent layer, and presentation layer.

## 2. Anti-Patterns Identified
- God class / low cohesion in the original parking manager
- UI logic tightly coupled to business logic
- Broken EV inheritance
- Duplicated EV vs. non-EV search and parking logic
- Primitive flag-based branching for vehicle type handling
- Inconsistent response handling (`True`/`False`/`-1`)

## 3. Design Patterns Used
### Factory Pattern
The `VehicleFactory` centralizes vehicle creation. New vehicle types can be added without modifying core parking logic.

### Capability-Based Slot Assignment / Polymorphism
Slots determine compatibility through their own `can_accept()` behavior. Vehicles expose their capabilities through properties such as `is_electric` and `is_autonomous`.

## 4. Architectural Improvements
- Vehicle hierarchy unified and corrected
- Separate services for parking, search, valet, and customer help
- Event bus added for observability and agent workflows
- Standardized structured responses for UI, CLI, and future APIs
- Agent gateway added for machine-readable tool execution

## 5. AI-Agent Readiness
The new architecture includes:
- Tool schemas
- Agent gateway
- Event history
- Structured entity serialization
- VIP/valet workflow support
- Customer-service requests

## 6. Domain-Driven Design
### Core Domain
Parking Management

### Subdomains
- Vehicle Management
- EV Charging / EV Status
- Valet & Reservations
- Customer Service

### Bounded Contexts
- Parking Context
- Vehicle Context
- Valet Context
- Customer Service Context
- Agent Interaction Context

## 7. Proposed Microservices
- Parking Service
- Vehicle Service
- Valet Service
- Customer Service
- Event / Notification Service
- Agent Gateway API

## 8. Submission Assets
- Refactored source code
- UML source diagrams
- Architecture write-up
- Working UI
- Working CLI
