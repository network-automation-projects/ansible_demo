"""
Netmiko / NAPALM starter — types and helpers for new tools
==========================================================

Copy or import from this file when building Netmiko or NAPALM tools so you get:
- IntelliSense (autocomplete) on connection objects
- Type checking for connection methods
- Safe connect → run → disconnect patterns

Usage:
  1. Import the Protocols and helpers you need.
  2. Type your connection params as NetmikoConnection or NAPALMConnection.
  3. Use run_with_netmiko() / run_with_napalm() for one-off tasks, or
     connect_netmiko() / connect_napalm() when you need to keep the connection.

  from netmiko_napalm_starter import (
      NetmikoConnection,
      NAPALMConnection,
      connect_netmiko,
      connect_napalm,
      run_with_netmiko,
      run_with_napalm,
  )

  # One-off: connect, run, disconnect
  result = run_with_netmiko(device_info, lambda conn: conn.send_command("show version"))

  # Or open connection and use it
  conn = connect_netmiko(device_info)
  try:
      out = conn.send_command("show ip int brief")
  finally:
      conn.disconnect()
"""

from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# =============================================================================
# Protocol types (for IntelliSense and type checking)
# =============================================================================


class NetmikoConnection(Protocol):
    """Protocol for Netmiko connection objects. Use to get type hint for IntelliSense."""

    def send_command(self, command_string: str, **kwargs: Any) -> str:
        ...

    def send_config_set(
        self, config_commands: List[str], **kwargs: Any
    ) -> str:
        ...

    def save_config(self, **kwargs: Any) -> None:
        ...

    def disconnect(self) -> None:
        ...


class NAPALMConnection(Protocol):
    """Protocol for NAPALM driver connection objects. Use as type hint for IntelliSense."""

    def get_facts(self) -> Dict[str, Any]:
        ...

    def get_interfaces(self) -> Dict[str, Dict[str, Any]]:
        ...

    def load_merge_candidate(self, config: str = "") -> None:
        ...

    def load_replace_candidate(self, filename: str = "", config: str = "") -> None:
        ...

    def compare_config(self) -> str:
        ...

    def commit_config(self, message: str = "") -> None:
        ...

    def discard_config(self) -> None:
        ...

    def close(self) -> None:
        ...


# =============================================================================
# Connection helpers
# =============================================================================

# Netmiko expects: host, username, password, device_type, optional secret, etc.
NetmikoDeviceInfo = Dict[str, str]

# NAPALM expects: hostname, username, password, driver (e.g. 'ios', 'eos', 'junos')
NAPALMDeviceInfo = Dict[str, str]

T = TypeVar("T")


def connect_netmiko(device_info: NetmikoDeviceInfo) -> NetmikoConnection:
    """
    Connect to a device using Netmiko.
    Caller must call conn.disconnect() when done (or use run_with_netmiko).
    """
    from netmiko import ConnectHandler

    conn = ConnectHandler(**device_info)
    return conn  # type: ignore[return-value]


def connect_napalm(device_info: NAPALMDeviceInfo) -> NAPALMConnection:
    """
    Connect to a device using NAPALM.
    Caller must call conn.close() when done (or use run_with_napalm).
    """
    import napalm

    driver = napalm.get_network_driver(device_info["driver"])
    conn = driver(
        hostname=device_info["hostname"],
        username=device_info["username"],
        password=device_info["password"],
        optional_args=device_info.get("optional_args") or {},
    )
    conn.open()
    return conn  # type: ignore[return-value]


def run_with_netmiko(
    device_info: NetmikoDeviceInfo,
    operation: Callable[[NetmikoConnection], T],
) -> T:
    """
    Connect with Netmiko, run operation(conn), then disconnect.
    Ensures disconnect() is called even if operation raises.
    """
    conn: Optional[NetmikoConnection] = None
    try:
        conn = connect_netmiko(device_info)
        return operation(conn)
    finally:
        if conn is not None and hasattr(conn, "disconnect"):
            try:
                conn.disconnect()
            except Exception as e:
                logger.warning("Error disconnecting Netmiko: %s", e)


def run_with_napalm(
    device_info: NAPALMDeviceInfo,
    operation: Callable[[NAPALMConnection], T],
) -> T:
    """
    Connect with NAPALM, run operation(conn), then close.
    Ensures close() is called even if operation raises.
    """
    conn: Optional[NAPALMConnection] = None
    try:
        conn = connect_napalm(device_info)
        return operation(conn)
    finally:
        if conn is not None and hasattr(conn, "close"):
            try:
                conn.close()
            except Exception as e:
                logger.warning("Error closing NAPALM connection: %s", e)


# =============================================================================
# Example usage (run this file to see patterns)
# =============================================================================

if __name__ == "__main__":
    # Example device dicts — replace with real credentials for live devices.
    # Never commit real credentials.

    netmiko_info: NetmikoDeviceInfo = {
        "host": "10.0.0.1",
        "username": "admin",
        "password": "secret",
        "device_type": "cisco_ios",
    }

    napalm_info: NAPALMDeviceInfo = {
        "hostname": "10.0.0.1",
        "username": "admin",
        "password": "secret",
        "driver": "ios",
    }

    # Pattern 1: One-off with run_with_netmiko (no manual disconnect)
    def show_version(conn: NetmikoConnection) -> str:
        return conn.send_command("show version")

    # Uncomment when you have a real device:
    # result = run_with_netmiko(netmiko_info, show_version)
    # print(result[:200])

    # Pattern 2: One-off with run_with_napalm
    def get_facts_and_close(conn: NAPALMConnection) -> Dict[str, Any]:
        return conn.get_facts()

    # Uncomment when you have a real device:
    # facts = run_with_napalm(napalm_info, get_facts_and_close)
    # print(facts)

    # Pattern 3: Manual connect / use / disconnect (when you need the connection longer)
    # conn = connect_netmiko(netmiko_info)
    # try:
    #     out = conn.send_command("show ip int brief")
    #     print(out)
    # finally:
    #     conn.disconnect()

    print("Starter loaded. Use run_with_netmiko / run_with_napalm or connect_* + try/finally.")
