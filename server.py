
"""
Cisco Network MCP Server
Python + FastMCP + Netmiko
Target: Cisco IOS / IOL lab devices
"""

from typing import List
from fastmcp import FastMCP
from netmiko import ConnectHandler

mcp = FastMCP("Cisco Network MCP Server")


# --------------------------------------------------
# Approved read-only SHOW commands
# --------------------------------------------------

ALLOWED_SHOW_COMMANDS = {
    # General
    "show version",
    "show inventory",
    "show clock",
    "show users",
    "show logging",
    "show running-config",
    "show startup-config",

    # Interfaces and Layer 2
    "show ip interface brief",
    "show ipv6 interface brief",
    "show interfaces",
    "show interfaces description",
    "show interfaces status",
    "show interfaces trunk",
    "show vlan brief",
    "show mac address-table",
    "show mac address-table dynamic",
    "show spanning-tree",
    "show spanning-tree summary",
    "show etherchannel summary",
    "show port-security",
    "show port-security interface",
    "show cdp neighbors",
    "show cdp neighbors detail",
    "show lldp neighbors",
    "show lldp neighbors detail",

    # IPv4 / IPv6 routing
    "show ip route",
    "show ipv6 route",
    "show ip protocols",
    "show ip arp",
    "show arp",
    "show ip cef",
    "show vrf",
    "show vrf brief",

    # OSPF
    "show ip ospf",
    "show ip ospf neighbor",
    "show ip ospf database",
    "show ip ospf interface",
    "show ip ospf interface brief",

    # BGP
    "show ip bgp summary",
    "show ip bgp",
    "show bgp ipv4 unicast summary",
    "show bgp ipv4 unicast",

    # EIGRP
    "show ip eigrp neighbors",
    "show ip eigrp topology",
    "show ip eigrp interfaces",

    # IS-IS
    "show isis neighbors",
    "show isis database",
    "show isis topology",
    "show clns neighbors",

    # Security and services
    "show access-lists",
    "show ip access-lists",
    "show ip nat translations",
    "show ip nat statistics",
    "show standby brief",
    "show ip ssh",
    "show users",
}


# --------------------------------------------------
# Connection helper
# --------------------------------------------------

def connect_device(
    device_ip: str,
    username: str,
    password: str,
    enable_secret: str = "",
):
    """Open an SSH connection to a Cisco IOS device."""

    if not device_ip.strip():
        raise ValueError("Device IP address cannot be empty.")

    if not username.strip():
        raise ValueError("Username cannot be empty.")

    if not password:
        raise ValueError("Password cannot be empty.")

    device = {
        "device_type": "cisco_ios",
        "host": device_ip.strip(),
        "username": username,
        "password": password,
        "secret": enable_secret or "",
        "conn_timeout": 10,
        "auth_timeout": 10,
        "banner_timeout": 10,
        "fast_cli": False,
    }

    return ConnectHandler(**device)


def execute_show(
    device_ip: str,
    username: str,
    password: str,
    command: str,
    enable_secret: str = "",
) -> str:
    """Execute one explicitly approved show command."""

    command = command.strip()

    if command not in ALLOWED_SHOW_COMMANDS:
        raise ValueError(
            "Command not allowed. Use an exact command "
            "from the approved SHOW command list."
        )

    connection = None

    try:
        connection = connect_device(
            device_ip,
            username,
            password,
            enable_secret,
        )

        # Enter privileged EXEC mode if necessary.
        if enable_secret:
            connection.enable()

        return connection.send_command(
            command,
            read_timeout=60,
        )

    finally:
        if connection is not None:
            connection.disconnect()


# --------------------------------------------------
# Tool 1: Interface status
# --------------------------------------------------

@mcp.tool()
def get_interface_status(
    device_ip: str,
    username: str,
    password: str,
    enable_secret: str = "",
) -> str:
    """Get the IPv4 interface summary from a Cisco IOS router or switch."""

    return execute_show(
        device_ip,
        username,
        password,
        "show ip interface brief",
        enable_secret,
    )


# --------------------------------------------------
# Tool 2: Running configuration
# --------------------------------------------------

@mcp.tool()
def get_running_config(
    device_ip: str,
    username: str,
    password: str,
    enable_secret: str = "",
) -> str:
    """Retrieve the running configuration of a Cisco IOS device."""

    return execute_show(
        device_ip,
        username,
        password,
        "show running-config",
        enable_secret,
    )


# --------------------------------------------------
# Tool 3: Approved SHOW command
# --------------------------------------------------

@mcp.tool()
def run_show_command(
    device_ip: str,
    username: str,
    password: str,
    command: str,
    enable_secret: str = "",
) -> str:
    """
    Run one exact, approved, read-only Cisco IOS SHOW command.

    The command must match an entry in ALLOWED_SHOW_COMMANDS.
    """

    return execute_show(
        device_ip,
        username,
        password,
        command,
        enable_secret,
    )


# --------------------------------------------------
# Tool 4: Configure device
# --------------------------------------------------

@mcp.tool()
def configure_device(
    device_ip: str,
    username: str,
    password: str,
    commands: List[str],
    confirm: bool,
    enable_secret: str = "",
) -> str:
    """
    Send configuration commands to a Cisco IOS lab device.

    Requires confirm=True. Configuration is not saved
    to startup-config automatically.

    Example commands:
    ["interface loopback10", "ip address 10.10.10.10 255.255.255.255"]

    Review the commands before execution.
    """

    if confirm is not True:
        return "Configuration cancelled: explicit confirmation is required."

    if not commands:
        raise ValueError("At least one configuration command is required.")

    if len(commands) > 100:
        raise ValueError("Maximum 100 configuration commands per call.")

    blocked_commands = {
        "end",
        "exit",
        "configure terminal",
        "conf t",
        "write",
        "write memory",
        "copy running-config startup-config",
        "reload",
        "erase startup-config",
        "delete",
    }

    cleaned_commands = []

    for command in commands:
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Every command must be a non-empty string.")

        command = command.strip()

        if "\n" in command or "\r" in command:
            raise ValueError("Each list item must contain only one command.")

        if command.lower() in blocked_commands:
            raise ValueError(
                f"Command '{command}' is blocked in this tool."
            )

        cleaned_commands.append(command)

    connection = None

    try:
        connection = connect_device(
            device_ip,
            username,
            password,
            enable_secret,
        )

        if not connection.check_enable_mode():
            connection.enable()

        output = connection.send_config_set(
            cleaned_commands,
            read_timeout=60,
            cmd_verify=True,
        )

        return (
            "Configuration commands sent.\n"
            "Review the device output below.\n"
            "Changes have NOT been explicitly saved "
            "to startup-config by this tool.\n\n"
            + output
        )

    finally:
        if connection is not None:
            connection.disconnect()


# --------------------------------------------------
# Tool 5: Save configuration
# --------------------------------------------------

@mcp.tool()
def save_configuration(
    device_ip: str,
    username: str,
    password: str,
    confirm: bool,
    enable_secret: str = "",
) -> str:
    """
    Save the current running configuration to startup-config.

    Requires confirm=True because saving changes affects
    the device's persistent configuration.
    """

    if confirm is not True:
        return "Save cancelled: explicit confirmation is required."

    connection = None

    try:
        connection = connect_device(
            device_ip,
            username,
            password,
            enable_secret,
        )

        if not connection.check_enable_mode():
            connection.enable()

        return connection.save_config()

    finally:
        if connection is not None:
            connection.disconnect()


# --------------------------------------------------
# Start MCP server
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run()
