import json
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

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

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Lot Manager - Final Submission")
        self.root.geometry("900x760")

        event_bus = EventBus()
        lot = build_demo_lot()
        parking_service = ParkingService(lot, event_bus)
        search_service = SearchService(lot)
        valet_service = ValetService(parking_service, event_bus)
        customer_service = CustomerService(search_service, parking_service)
        self.gateway = AgentGateway(parking_service, valet_service, customer_service, event_bus)

        self.vehicle_type = tk.StringVar(value="car")
        self.regnum = tk.StringVar()
        self.make = tk.StringVar()
        self.model = tk.StringVar()
        self.color = tk.StringVar()
        self.customer_id = tk.StringVar(value="cust_001")
        self.priority = tk.StringVar(value="standard")
        self.help_type = tk.StringVar(value="get_lot_status")
        self.help_regnum = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Parking Lot Manager", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        labels = [
            ("Vehicle Type", self.vehicle_type),
            ("Registration", self.regnum),
            ("Make", self.make),
            ("Model", self.model),
            ("Color", self.color),
            ("Customer ID", self.customer_id),
            ("Priority", self.priority),
        ]

        for i, (label, var) in enumerate(labels, start=1):
            ttk.Label(frm, text=label).grid(row=i, column=0, sticky="w", pady=4)
            if label == "Vehicle Type":
                ttk.Combobox(frm, textvariable=var, values=[
                    "car", "motorcycle", "truck", "bus",
                    "electric_car", "electric_bike",
                    "autonomous_car", "autonomous_electric_car"
                ], state="readonly").grid(row=i, column=1, sticky="ew", pady=4)
            elif label == "Priority":
                ttk.Combobox(frm, textvariable=var, values=["standard", "vip"], state="readonly").grid(row=i, column=1, sticky="ew", pady=4)
            else:
                ttk.Entry(frm, textvariable=var).grid(row=i, column=1, sticky="ew", pady=4)

        ttk.Button(frm, text="Park Vehicle", command=self.park_vehicle).grid(row=1, column=2, padx=10, sticky="ew")
        ttk.Button(frm, text="Request Valet", command=self.request_valet).grid(row=2, column=2, padx=10, sticky="ew")
        ttk.Button(frm, text="Lot Status", command=self.get_lot_status).grid(row=3, column=2, padx=10, sticky="ew")
        ttk.Button(frm, text="EV Charge Status", command=self.get_ev_status).grid(row=4, column=2, padx=10, sticky="ew")
        ttk.Button(frm, text="Event History", command=self.get_events).grid(row=5, column=2, padx=10, sticky="ew")

        ttk.Label(frm, text="Customer Help Type").grid(row=9, column=0, sticky="w", pady=(16, 4))
        ttk.Combobox(frm, textvariable=self.help_type, values=["get_lot_status", "get_ev_charge_status", "find_vehicle"], state="readonly").grid(row=9, column=1, sticky="ew", pady=(16, 4))
        ttk.Label(frm, text="Help Registration").grid(row=10, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.help_regnum).grid(row=10, column=1, sticky="ew", pady=4)
        ttk.Button(frm, text="Run Customer Help", command=self.run_customer_help).grid(row=10, column=2, padx=10, sticky="ew")

        ttk.Label(frm, text="Output").grid(row=11, column=0, sticky="w", pady=(16, 4))
        self.output = tk.Text(frm, width=110, height=26)
        self.output.grid(row=12, column=0, columnspan=4, sticky="nsew")

        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(12, weight=1)

    def _vehicle_payload(self):
        payload = {
            "vehicle_type": self.vehicle_type.get(),
            "regnum": self.regnum.get().strip(),
            "make": self.make.get().strip(),
            "model": self.model.get().strip(),
            "color": self.color.get().strip(),
        }
        missing = [k for k in ["regnum", "make", "model", "color"] if not payload[k]]
        if missing:
            messagebox.showerror("Missing data", "Please fill in registration, make, model, and color.")
            return None
        return payload

    def _render(self, result):
        self.output.insert("end", json.dumps(result, indent=2) + "\n\n")
        self.output.see("end")

    def park_vehicle(self):
        payload = self._vehicle_payload()
        if payload:
            self._render(self.gateway.execute("park_vehicle", payload))

    def request_valet(self):
        payload = self._vehicle_payload()
        if payload:
            payload["customer_id"] = self.customer_id.get().strip() or "cust_001"
            payload["priority"] = self.priority.get()
            self._render(self.gateway.execute("request_valet", payload))

    def get_lot_status(self):
        self._render(self.gateway.execute("get_customer_help", {"request_type": "get_lot_status"}))

    def get_ev_status(self):
        self._render(self.gateway.execute("get_customer_help", {"request_type": "get_ev_charge_status"}))

    def run_customer_help(self):
        payload = {"request_type": self.help_type.get()}
        if self.help_type.get() == "find_vehicle":
            payload["regnum"] = self.help_regnum.get().strip()
        self._render(self.gateway.execute("get_customer_help", payload))

    def get_events(self):
        self._render(self.gateway.execute("list_events", {}))

def main():
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
