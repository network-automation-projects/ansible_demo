"""
Python Network Automation - BASIC Decorators Exercise
=================================================
"""

class NetworkDevice:
    def __init__(self, hostname, ip, username, password):
        self._hostname = hostname
        self._ip = ip
        self._username = username
        self._password = password
        self._connected = False  # protected attribute

    @property
    def status(self):
        """Read-only property: returns connection status as a string."""
        return "Connected" if self._connected else "Disconnected"

    @property
    def credentials_safe(self):
        """Example: hide password, return safe representation."""
        return f"{self._username}@********"

    def connect(self):
        self._connected = True  # simulate
        print(f"Connected to {self._hostname}")

# Usage
dev = NetworkDevice("router1", "10.0.0.1", "admin", "secret")
print(dev.status)          # → Disconnected (no () needed)
dev.connect()
print(dev.status)          # → Connected
print(dev.credentials_safe)  # → admin@********