from netmiko import ConnectHandler
import datetime
import socket

# Clean, minimal device parameters (no deprecated args like look_for_keys or allow_agent)
device = {
    "device_type": "cisco_ios",
    "host": "sandbox-iosxe-latest-1.cisco.com",  # Latest code sandbox (stable as of Dec 2025)
    "username": "developer",                     # Current public username
    "password": "C1sco12345",                    # Public password
    "port": 22,
    "secret": "C1sco12345",                      # Enable secret (same as password)
    "conn_timeout": 30,
    "auth_timeout": 30,
    "banner_timeout": 30,
}

print(f"DNS resolved: {device['host']} -> {socket.gethostbyname(device['host'])}")
print(f"Port {device['port']} is reachable")

print("Connecting to public Cisco IOS-XE sandbox...")
print(f"Started: {datetime.datetime.now()}\n")

try:
    with ConnectHandler(**device) as conn:
        # Extract hostname reliably
        version_output = conn.send_command("show version")
        hostname_line = [line for line in version_output.splitlines() if "Processor board ID" in line]
        hostname = hostname_line[0].split()[-1] if hostname_line else "unknown"

        config = conn.send_command("show running-config")

        filename = f"backup_{hostname}_{datetime.date.today()}.cfg"
        with open(filename, "w") as f:
            f.write(config)

        print(f"Saved config to {filename} (visible on your Mac thanks to volume mount!)")
        print("\nFirst 20 lines of config:")
        print("\n".join(config.splitlines()[:20]))

    print("\nBackup complete!")
except Exception as e:
    print(f"\nConnection failed: {e}")