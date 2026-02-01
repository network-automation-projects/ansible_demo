"""
Netmiko connection runner: build params, command mapping, run_command with optional mock.
"""

import os
from pathlib import Path
from typing import Any

import yaml

# Netmiko imports (only used when connect_func is None)
try:
    from netmiko import (
        ConnectHandler,
        NetmikoAuthenticationException,
        NetmikoTimeoutException,
    )
except ImportError:
    ConnectHandler = None
    NetmikoTimeoutException = Exception
    NetmikoAuthenticationException = Exception


def build_netmiko_params(device: dict[str, Any]) -> dict[str, Any]:
    """Convert inventory device dict to ConnectHandler kwargs."""
    params: dict[str, Any] = {
        "device_type": device["device_type"],
        "host": device["ip"],
        "username": device.get("username") or os.environ.get("NET_USER", ""),
        "password": device.get("password") or os.environ.get("NET_PASS", ""),
    }
    if device.get("secret"):
        params["secret"] = device["secret"]
    if device.get("port"):
        params["port"] = device["port"]
    return params


def get_show_version_command(device_type: str) -> str:
    """Map device_type to vendor-specific 'show version' command."""
    mapping = {
        "cisco_ios": "show version",
        "cisco_nxos": "show version",
        "cisco_xr": "show version",
        "juniper_junos": "show version",
        "arista_eos": "show version",
        "nokia_srl": "show system information",
    }
    return mapping.get(device_type, "show version")


def run_command(
    device: dict[str, Any],
    command: str,
    *,
    connect_func: Any = None,
) -> str | None:
    """Connect (or use connect_func mock), optionally enable, send command. Return output or None on exception."""
    params = build_netmiko_params(device)
    needs_enable = device.get("device_type", "") not in (
        "juniper_junos",
        "nokia_srl",
    )

    if connect_func is not None:
        with connect_func(params) as conn:
            if needs_enable:
                conn.enable()
            return conn.send_command(command)

    if ConnectHandler is None:
        return None

    try:
        with ConnectHandler(**params) as conn:
            if needs_enable:
                conn.enable()
            return conn.send_command(command)
    except (NetmikoTimeoutException, NetmikoAuthenticationException, Exception):
        return None


def load_devices(inventory_path: Path) -> list[dict[str, Any]]:
    """Load devices from YAML inventory."""
    with open(inventory_path) as f:
        data = yaml.safe_load(f)
    return data.get("devices", [])


def _make_mock_conn(fixture_path: Path):
    """Return a connect_func that yields a mock connection returning fixture content."""

    class MockConn:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def enable(self):
            pass

        def send_command(self, cmd: str) -> str:
            return fixture_path.read_text()

    return lambda params: MockConn()


def main() -> None:
    base = Path(__file__).parent
    inventory = base / "minimal" / "devices.yaml"
    fixture_path = base / "fixtures" / "show_version_sample.txt"

    devices = load_devices(inventory)
    use_mock = os.environ.get("NETMIKO_USE_MOCK", "").strip() == "1" or not devices

    if use_mock:
        mock_device = {"ip": "127.0.0.1", "device_type": "cisco_ios"}
        command = get_show_version_command("cisco_ios")
        output = run_command(
            mock_device, command, connect_func=_make_mock_conn(fixture_path)
        )
        print("Running in MOCK mode (no real device)")
    else:
        device = devices[0]
        command = get_show_version_command(device["device_type"])
        output = run_command(device, command)
        print(f"Running against {device.get('hostname', device['ip'])}")

    if output is None:
        print("FAILED: no output (connection or auth error)")
    else:
        print("OK")
        lines = output.strip().splitlines()
        for line in lines[:5]:
            print(f"  {line}")
        if len(lines) > 5:
            print("  ...")


if __name__ == "__main__":
    main()
