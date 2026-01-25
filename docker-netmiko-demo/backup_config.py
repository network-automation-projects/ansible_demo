from netmiko import ConnectHandler
import datetime

device = {
    "device_type": "cisco_ios",
    "host": "sandbox-iosxe-recomm-1.cisco.com",
    "username": "developer",
    "password": "C1sco12345",
    "port": 22,
}

print("Connecting to real Cisco IOS-XE sandbox router...")
print(f"Backup started: {datetime.datetime.now()}\n")

with ConnectHandler(**device) as conn:
    hostname = conn.send_command("show version | include Processor").split()[-1]
    config = conn.send_command("show running-config")
    
    filename = f"backup_{hostname}_{datetime.date.today()}.cfg"
    with open(filename, "w") as f:
        f.write(config)
    
    print(f"Saved config to {filename} (visible on your Mac!)")
    print("\nFirst 20 lines of real router config:")
    print("\n".join(config.splitlines()[:20]))

print("\nBackup complete!")