import paramiko
import time

def configure_bgp(hostname, username, password, as_number, neighbors, networks):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the router
        ssh_client.connect(hostname, username=username, password=password)
        print(f"Connected to {hostname}")
        
        # Invoke a shell
        remote_connection = ssh_client.invoke_shell()
        
        # Enter configuration mode
        remote_connection.send("configure terminal\n")
        time.sleep(1)
        
        # Configure BGP
        remote_connection.send(f"router bgp {as_number}\n")
        time.sleep(1)
        
        # Add neighbors
        for neighbor_ip, neighbor_as, update_source, ebgp_multihop in neighbors:
            remote_connection.send(f"neighbor {neighbor_ip} remote-as {neighbor_as}\n")
            time.sleep(1)
            if update_source:
                remote_connection.send(f"neighbor {neighbor_ip} update-source {update_source}\n")
                time.sleep(1)
            if ebgp_multihop:
                remote_connection.send(f"neighbor {neighbor_ip} ebgp-multihop {ebgp_multihop}\n")
                time.sleep(1)
        
        # Add networks
        for network, mask in networks:
            remote_connection.send(f"network {network} mask {mask}\n")
            time.sleep(1)
        
        remote_connection.send("no auto-summary\n")
        time.sleep(1)
        
        # Verify the configuration
        remote_connection.send("end\n")
        time.sleep(1)
        remote_connection.send("show ip bgp\n")
        time.sleep(2)
        
        # Receive the output
        output = remote_connection.recv(65535).decode("utf-8")
        print(output)
        
        # Close the connection
        ssh_client.close()
        print(f"Disconnected from {hostname}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Gather user input
hostname = input("Enter the router IP address: ")
username = input("Enter your username: ")
password = input("Enter your password: ")
as_number = input("Enter your AS number: ")

# Get neighbor details
neighbors = []
num_neighbors = int(input("How many neighbors do you want to add :  "))
for _ in range(num_neighbors):
    neighbor_ip = input("Enter the neighbor IP address: ")
    neighbor_as = input("Enter the neighbor AS number: ")
    update_source = input("Enter the update source interface (or press Enter to skip): ")
    ebgp_multihop = input("Enter the eBGP multihop value (or press Enter to skip): ")
    neighbors.append((neighbor_ip, neighbor_as, update_source, ebgp_multihop))

# Get network details
networks = []
num_networks = int(input("How many networks do you want to add? "))
for _ in range(num_networks):
    network = input("Enter the network IP: ")
    mask = input("Enter the subnet mask: ")
    networks.append((network, mask))

# Configure BGP
configure_bgp(hostname, username, password, as_number, neighbors, networks)
