class NetDevices:
    def __init__(self, model, version, ip_mgmt):
        self.model = model
        self.version = version
        self.ip_mgmt = ip_mgmt

    def show_info(self):
        print(f"Model: {self.model}")
        print(f"Software Version: {self.version}")
        print(f"Management IP: {self.ip_mgmt}")


class Router(NetDevices):
    def __init__(self, model, version, ip_mgmt, routing_protocol):
        super().__init__(model, version, ip_mgmt)
        self.routing_protocol = routing_protocol

    def show_info(self):
        print("=== Router ===")
        super().show_info()
        print(f"Routing Protocol: {self.routing_protocol}")


class Switch(NetDevices):
    def __init__(self, model, version, ip_mgmt, vlan):
        super().__init__(model, version, ip_mgmt)
        self.vlan = vlan

    def show_info(self):
        print("=== Switch ===")
        super().show_info()
        print(f"Management VLAN: {self.vlan}")


r1 = Router(
    "Cisco ISR 4331",
    "17.9.4",
    "10.10.10.1",
    "OSPF"
)

sw1 = Switch(
    "Cisco Catalyst 9300",
    "17.9.4",
    "10.10.10.2",
    10
)

sw2 = Switch(
    "Cisco Catalyst 9000",
    "15.1.0",
    "192.168.1.1.",
    20
)
r1.show_info()
sw1.show_info()
sw2.show_info()