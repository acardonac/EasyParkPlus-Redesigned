AGENT_TOOL_SCHEMAS = {
    "park_vehicle": {
        "description": "Park a supported vehicle in the first compatible available slot.",
        "input_schema": {
            "vehicle_type": "string",
            "regnum": "string",
            "make": "string",
            "model": "string",
            "color": "string"
        }
    },
    "request_valet": {
        "description": "Create a standard or VIP valet reservation and park the vehicle.",
        "input_schema": {
            "customer_id": "string",
            "priority": "string",
            "vehicle_type": "string",
            "regnum": "string",
            "make": "string",
            "model": "string",
            "color": "string"
        }
    },
    "get_customer_help": {
        "description": "Handle customer-service tasks such as finding a vehicle or getting lot status.",
        "input_schema": {
            "request_type": "string",
            "regnum": "string (optional)"
        }
    },
    "list_events": {
        "description": "Return emitted application events.",
        "input_schema": {}
    }
}

class AgentPolicyEngine:
    def __init__(self):
        self.restricted_actions = set()

    def is_allowed(self, action: str, params: dict) -> bool:
        return action not in self.restricted_actions

class AgentGateway:
    def __init__(self, parking_service, valet_service, customer_service, event_bus, policy_engine=None):
        self.parking_service = parking_service
        self.valet_service = valet_service
        self.customer_service = customer_service
        self.event_bus = event_bus
        self.policy_engine = policy_engine or AgentPolicyEngine()

    def get_tool_schemas(self):
        return AGENT_TOOL_SCHEMAS

    def execute(self, action: str, params: dict):
        if not self.policy_engine.is_allowed(action, params):
            return {
                "success": False,
                "message": f"Action '{action}' is not allowed.",
                "error_code": "ACTION_NOT_ALLOWED",
                "data": None,
            }

        if action == "park_vehicle":
            return self.parking_service.park_vehicle(**params)
        if action == "request_valet":
            return self.valet_service.request_valet(**params)
        if action == "get_customer_help":
            return self.customer_service.handle_request(**params)
        if action == "list_events":
            return {
                "success": True,
                "message": "Event history retrieved.",
                "error_code": None,
                "data": {"events": self.event_bus.list_events()},
            }
        return {
            "success": False,
            "message": f"Unknown action: {action}",
            "error_code": "UNKNOWN_ACTION",
            "data": None,
        }
