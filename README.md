# Final Submission Version - Parking Lot Manager

This package contains a project-ready refactor of the original parking lot prototype.

## Included
- Modular Python source code
- Tkinter UI version
- CLI version
- AI Agent Gateway
- Valet/VIP service
- Customer-service layer
- Event bus
- Agent manifest (`SKILL.md`)
- Tool schemas
- UML source (`docs/uml/*.puml`)
- Project report draft (`docs/Project_Report_Draft.md`)
- Architecture summary

## Run the Tkinter app
```bash
python src/ParkingManager.py
```

## Run the CLI version
```bash
python src/cli_main.py park_vehicle --params "{\"vehicle_type\": \"electric_car\", \"regnum\": \"ABC123\", \"make\": \"Tesla\", \"model\": \"Model 3\", \"color\": \"Red\"}"
```

## Notes
This redesign makes the system easier to extend with:
- electric bikes
- autonomous vehicles
- valet/VIP workflows
- AI-agent tool invocation
- future API integration
