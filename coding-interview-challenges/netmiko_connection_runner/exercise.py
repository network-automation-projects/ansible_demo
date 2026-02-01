"""
Exercise: Netmiko connection params, command mapping, run_command with optional mock.
Fill in the TODOs. See README.md for the problem description.
"""

import os
from pathlib import Path
from typing import Any

import yaml


def build_netmiko_params(device: dict[str, Any]) -> dict[str, Any]:
    """Convert inventory device dict to ConnectHandler kwargs (host, device_type, username, password, secret, port)."""
    # TODO: params = {"device_type": device["device_type"], "host": device["ip"]}
    # TODO: username = device.get("username") or os.environ.get("NET_USER", "")
    # TODO: password = device.get("password") or os.environ.get("NET_PASS", "")
    # TODO: add secret if device has it; add port if device has it
    raise NotImplementedError("TODO: implement build_netmiko_params")


def get_show_version_command(device_type: str) -> str:
    """Map device_type to vendor-specific 'show version' command."""
    # TODO: mapping for cisco_ios, cisco_nxos, cisco_xr, juniper_junos, arista_eos, nokia_srl
    # TODO: nokia_srl uses "show system information"; juniper uses "show version"; rest use "show version"
    raise NotImplementedError("TODO: implement get_show_version_command")


def run_command(
    device: dict[str, Any],
    command: str,
    *,
    connect_func: Any = None,
) -> str | None:
    """Connect (or use connect_func mock), optionally enable, send command. Return output or None on exception."""
    # TODO: params = build_netmiko_params(device)
    # TODO: if connect_func: call it as mock - return fixture content for "show version" or similar
    # TODO: else: from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
    # TODO:   with ConnectHandler(**params) as conn:
    # TODO:     if device needs enable (cisco, arista - not juniper, nokia_srl): conn.enable()
    # TODO:     return conn.send_command(command)
    # TODO:   except NetmikoTimeoutException, NetmikoAuthenticationException, etc: return None
    raise NotImplementedError("TODO: implement run_command")


def load_devices(inventory_path: Path) -> list[dict[str, Any]]:
    """Load devices from YAML inventory. Return list of device dicts."""
    with open(inventory_path) as f:
        data = yaml.safe_load(f)
    return data.get("devices", [])


def main() -> None:
    base = Path(__file__).parent
    inventory = base / "minimal" / "devices.yaml"
    fixture_path = base / "fixtures" / "show_version_sample.txt"

    devices = load_devices(inventory)
    use_mock = os.environ.get("NETMIKO_USE_MOCK", "").strip() == "1" or not devices

    if use_mock:
        # TODO: create mock connect_func that reads fixture_path and returns content
        # TODO: create a minimal device dict for the mock (e.g. cisco_ios)
        # TODO: output = run_command(device, get_show_version_command("cisco_ios"), connect_func=mock)
        pass
    else:
        # TODO: device = devices[0]; command = get_show_version_command(device["device_type"])
        # TODO: output = run_command(device, command)
        pass

    # TODO: print success/failure and first 3 lines of output
    pass


if __name__ == "__main__":
    main()
