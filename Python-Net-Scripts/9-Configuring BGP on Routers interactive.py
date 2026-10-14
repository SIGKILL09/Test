from netmiko import ConnectHandler

# Function to establish SSH connection
def establish_ssh_connection(router):
    try:
        ssh_connection = ConnectHandler(**router)
        return ssh_connection
    except Exception as e:
        print(f"Failed to connect to the device. Error: {str(e)}")
        return None

# Function to configure BGP
def configure_bgp(ssh_connection):
    try:
        # Retrieve hostname of the router
        hostname_output = ssh_connection.send_command('show run | i hostname')
        hostname = hostname_output.split()[1]

        # Enter AS number
        as_num = input('Enter your AS number: ')
        router_bgp = f'router bgp {as_num}'
        config_commands = [router_bgp]

        # Configure networks to advertise
        network_y = input('Would you like to advertise networks [y/n]: ')
        if network_y.lower() == 'y':
            network_num = int(input('How many networks would you like to advertise: '))
            for _ in range(network_num):
                network_i = input('Network address [Ex: 199.1.1.0]: ')
                network_m = input('Subnet Mask: [255.255.255.0]: ')
                network_adv = f'network {network_i} mask {network_m}'
                config_commands.append(network_adv)

        # Configure BGP neighbors
        neighbor_num = int(input('How many neighbors would you like to configure: '))
        for _ in range(neighbor_num):
            remote_ip = input('Neighbor IP: ')
            remote_as = input('Remote AS: ')
            neighbor_cmd = f'neighbor {remote_ip} remote-as {remote_as}'
            config_commands.append(neighbor_cmd)

            # Optionally configure Update Source Interface
            update_source = input('Would you like to specify the Update-Source Interface [y/n]: ')
            if update_source.lower() == 'y':
                update_source_int = input('Enter the Update Source Interface [Loopback10]: ')
                neighbor_update_source = f'neighbor {remote_ip} update-source {update_source_int}'
                config_commands.append(neighbor_update_source)

            # Optionally configure eBGP Multihop
            ebgp_multihop = input('Would you like to specify the eBGP Multihop option [y/n]: ')
            if ebgp_multihop.lower() == 'y':
                multihop_ttl = input('Enter the eBGP Multihop TTL value [e.g., 2]: ')
                neighbor_ebgp_multihop = f'neighbor {remote_ip} ebgp-multihop {multihop_ttl}'
                config_commands.append(neighbor_ebgp_multihop)

            # Optionally configure Next-Hop-Self
            next_hop_self = input('Would you like to specify the Next-Hop-Self option [y/n]: ')
            if next_hop_self.lower() == 'y':
                neighbor_next_hop_self = f'neighbor {remote_ip} next-hop-self'
                config_commands.append(neighbor_next_hop_self)

            # Optionally configure Route Reflector
            route_ref = input('Would you like to specify the Route Reflector option [y/n]: ')
            if route_ref.lower() == 'y':
                neighbor_rr = f'neighbor {remote_ip} route-reflector-client'
                config_commands.append(neighbor_rr)

        # Send BGP configuration commands
        output = ssh_connection.send_config_set(config_commands)
        print(output)

    except Exception as e:
        print(f"Failed to configure BGP. Error: {str(e)}")

# Main function
def main():
    # Get number of routers to configure
    router_num = int(input("How many routers would you like to configure: "))

    for _ in range(router_num):
        hostip = input('Router IP: ')
        user = input('SSH Username: ')
        password = input('SSH Password: ')

        # Define router parameters
        router = {
            'device_type': 'cisco_ios',
            'ip': hostip,
            'username': user,
            'password': password
        }

        # Establish SSH connection to the router
        ssh_connection = establish_ssh_connection(router)
        if ssh_connection:
            configure_bgp(ssh_connection)
            ssh_connection.disconnect()

# Execute the main function
if __name__ == "__main__":
    main()
print("......end.......")
