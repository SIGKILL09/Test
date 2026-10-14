from getpass import getpass
from netmiko import ConnectHandler
password = getpass()
cisco_rtr = {
    'device_type': 'cisco_ios',
    'host' : '192.168.100.63',
    'username':'admin',
    'password':password,
    'port': 22,
    'secret':'',
}
cisco_rtr1 = {
    'device_type': 'cisco_ios',
    'host' : '192.168.100.64',
    'username':'admin',
    'password':password,
    'port': 22,
    'secret':'',
}


net_connect = ConnectHandler(**cisco_rtr)
net_connect = ConnectHandler(**cisco_rtr1)
print("SSH secessfull")
config = ['int loop 1','ip add 1.1.1.1 255.255.255.255','desc "By Netmiko']
config2 = ['int loop 2','ip add 2.1.1.1 255.255.255.255','desc "By Netmiko."']
static = ['ip route 0.0.0.0 0.0.0.0 192.168.100.254']
ping = ['do ping 8.8.8.8']
loop1 = net_connect.send_config_set(config)
loop2 = net_connect.send_config_set(config2)
static = net_connect.send_config_set(static)
show = net_connect.send_command('show ip int b')
show2 = net_connect.send_command('show ip route')
show3 = net_connect.send_command('show int status')
ping = net_connect.send_config_set(ping)
print(loop1)
print(loop2)
print(static)
print(show)
print(show2)
print(show3)
print(ping)
