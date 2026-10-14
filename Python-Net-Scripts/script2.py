from netmiko import ConnectHandler

switches = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.8.101",
        "username": "admin",
        "password": "Test123",
        "secret": "Test123",
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.8.102",
        "username": "admin",
        "password": "Test123",
        "secret": "Test123",
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.8.103",
        "username": "admin",
        "password": "Test123",
        "secret": "Test123",
    }
]

for switch in switches:
    net_connect = ConnectHandler(**switch)

    net_connect.enable()

    output = net_connect.send_command("show vlan brief")
    print(output)

    for vlan in range(10, 51, 10):
        config_commands = ["vlan " + str(vlan), "name Netmiko_VLAN_" + str(vlan)]
        output = net_connect.send_config_set(config_commands)
        print(output)

    output = net_connect.send_command("show vlan brief")
    print(output)

    net_connect.disconnect()