from netmiko import ConnectHandler

# Define the devices and their IP addresses
devices = {
    'sw1': '192.168.100.200'
    
}

# Common device parameters
common_params = {
    'device_type': 'cisco_ios',  # Assuming Cisco IOS devices
    'username': 'admin',  # Replace with your username
    'password': 'Test123',  # Replace with your password
    'secret': 'Test123',      # Replace with your secret
}

# VLAN configuration commands
vlan_commands = [
    'vlan 100',
    'name Marketing',
    'vlan 200',
    'name Sales',
    'vlan 300',
    'name Engineering',
    'vlan 400',
    'name HR',
]

# Iterate over the devices and configure VLANs
for device_name, ip_address in devices.items():
    # Update the device parameters with the specific IP address
    device_params = common_params.copy()
    device_params.update({'ip': ip_address})
    
    # Connect to the device
    print(f"Connecting to {device_name} at {ip_address}")
    net_connect = ConnectHandler(**device_params)
    net_connect.enable()
    
    # Send the VLAN configuration commands
    output = net_connect.send_config_set(vlan_commands)
    print(output)
    
    # Disconnect from the device
    net_connect.disconnect()
    print(f"Disconnected from {device_name}")

print("VLAN configuration completed on all switches.")