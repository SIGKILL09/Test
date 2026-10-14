from netmiko import ConnectHandler

# List of switches
switches = ['192.168.8.101', '192.168.8.102', '192.168.8.103']

# SSH credentials
username = 'admin'
password = 'Test123'

# VLAN configuration commands
vlan_commands = [
    'vlan 10',
    'name Netmiko_VLAN_10',
    'exit',
    'vlan 20',
    'name Netmiko_VLAN_20',
    'exit',
   'vlan 30',
    'name Netmiko_VLAN_30',
    'exit',
    'vlan 40',
    'name Netmiko_VLAN_40',
    'exit',
   'vlan 50',
    'name Netmiko_VLAN_50',
    'exit',
]

for ip in switches:
    device = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
    }

    # Establishing connection and sending configuration commands
    with ConnectHandler(**device) as conn:
        print(f"Connected to switch {ip}")
        output = conn.send_config_set(vlan_commands)
        print(output)
