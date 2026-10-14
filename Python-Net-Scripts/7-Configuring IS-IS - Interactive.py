from netmiko import ConnectHandler

router_num = input("How many routers would you like to configure: ")
router_num = int(router_num)

while router_num > 0:
    hostip = input('Router IP: ')
    USER = input('SSH Username: ')
    PASS = input('SSH Password: ')
    Router = {
        'device_type': 'cisco_ios',
        'ip': hostip,
        'username': USER,
        'password': PASS
    }

    myssh = ConnectHandler(**Router)
    hostname = myssh.send_command('show run | i host')
    x = hostname.split()
    device = x[1]

    isis_area = input('Area ID [4-hex Digit]: ')
    isis_system = input('System ID [xxxx.xxxx.xxxx]: ')
    isis_net = 'net 49.' + isis_area + '.' + isis_system + '.00'

    isis_level = input('IS-IS Type [Level-1 | level-2 | Level-1-2]: ')
    if isis_level.lower() == 'level-1':
        config_commands = ['router isis',
                            isis_net,
                            'is-type level-1']
    elif isis_level.lower() == 'level-2':
        config_commands = ['router isis',
                            isis_net,
                            'is-type level-2']
    else:
        config_commands = ['router isis',
                            isis_net ]


    output = myssh.send_config_set(config_commands)

    network_num = input('How many interfaces would you like to enable in IS-IS: ')
    network_num = int(network_num)
    while network_num > 0:
        network_i = input('Please specify the Interface to enable[loopback0,ethernet0/0 etc]: ')
        isis_interface = 'interface ' + network_i
        config_commands = [isis_interface,
                           'ip router isis']
        output = myssh.send_config_set(config_commands)
        print(output)
        network_num -=1

    print('Router \"' + device + '\" configured')
    print('-'*79)
    router_num -=1

input("Press ENTER to finish")