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
    ospfprocid = myssh.send_command('show run | i router ospf')
    x = hostname.split()
    device = x[1]

    area_num = input('How many areas would you like to configure: ')
    area_num = int(area_num)

    abr = input('Is the router an ABR: (y/n): ')

    while area_num > 0:
        area_id = input ('Input the Area ID: ')
        area_type = input('Specify Area Type for  ' + area_id + ' [Stub | NSSA | Totally Stubby | NSSA - Stub | NSSA - Totally Stub]: ')
        if area_type.lower() == 'stub':
            areacommand = 'area ' + area_id + ' stub'
            config_commands = [ospfprocid, areacommand]
        elif area_type.lower() == 'nssa':
            areacommand = 'area ' + area_id + ' nssa'
            config_commands = [ospfprocid, areacommand]
        elif abr == 'y' and area_type.lower() == 'totally stubby':
            areacommand = 'area ' + area_id + ' stub no-summary'
            config_commands = [ospfprocid, areacommand]
        elif abr == 'n' and area_type.lower() == 'totally stubby':
            areacommand = 'area ' + area_id + ' stub'
            config_commands = [ospfprocid, areacommand]
        elif abr == 'y' and area_type.lower() == 'nssa - stub':
            areacommand = 'area ' + area_id + ' nssa default-information-originate'
            config_commands = [ospfprocid, areacommand]
        elif abr == 'n' and area_type.lower() == 'nssa - stub':
            areacommand = 'area ' + area_id + ' nssa'
            config_commands = [ospfprocid, areacommand]
        elif abr == 'y' and area_type.lower() == 'nssa - totally stub':
            areacommand = 'area ' + area_id + ' nssa no-summary'
            config_commands = [ospfprocid, areacommand]
        elif abr == 'n' and area_type.lower() == 'nssa - totally stub':
            areacommand = 'area ' + area_id + ' nssa'
            config_commands = [ospfprocid, areacommand]

        output = myssh.send_config_set(config_commands)
        print(output)
        area_num -=1
    router_num -=1
    print('Router "' + device + '" configured')
    print('-' * 79)

input("Press ENTER to finish")