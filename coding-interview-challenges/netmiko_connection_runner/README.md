# Netmiko Connection Runner (Python)

Practice exercise for **Netmiko** and network device automation. Focus: build ConnectHandler params, map vendor-specific commands, run show commands with optional mock mode for device-less practice.

## What You'll Use

- **netmiko:** `ConnectHandler`, `send_command()`, `enable()`, `find_prompt()`
- **Exception handling:** `NetmikoTimeoutException`, `NetmikoAuthenticationException`
- **Context manager:** `with ConnectHandler(**params) as conn:`
- **Injectable connector:** Pass a mock function instead of real ConnectHandler for testing without devices

## Problem

1. **build_netmiko_params(device: dict) -> dict**  
   Convert an inventory device dict (hostname, ip, device_type, username, password, secret, port) into kwargs for `ConnectHandler`. Map keys: `ip` → `host`. Use `os.environ.get("NET_USER")` and `os.environ.get("NET_PASS")` if username/password are missing from the device. Include `secret` (enable password) if present. Include `port` if present (default 22).

2. **get_show_version_command(device_type: str) -> str**  
   Map device_type to the vendor-specific "show version" command. Support: `cisco_ios`, `cisco_nxos`, `cisco_xr`, `juniper_junos`, `arista_eos`, `nokia_srl`. Default to `"show version"` for unknown types.

3. **run_command(device: dict, command: str, *, connect_func=None) -> str | None**  
   Connect to the device and run the command. If `connect_func` is provided, use it as a mock (call it with params and return fixture output). Otherwise use real `ConnectHandler`. Enter enable mode for Cisco/Arista (not for juniper, nokia_srl). Return command output or `None` on exception.

4. **main()**  
   Load devices from `minimal/devices.yaml`. If `NETMIKO_USE_MOCK=1` or devices list is empty, use a mock that returns `fixtures/show_version_sample.txt` content. Otherwise run `show version` against the first device. Print success/failure and output snippet.

## Files

- **fixtures/show_version_sample.txt** – Sample Cisco IOS `show version` output for mock mode.
- **minimal/devices.yaml** – Device inventory (empty for mock; add device for real run).
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py`.
- **requirements.txt** – `netmiko>=4.0.0`.

## How to Practice

1. Read this README and install: `pip install -r requirements.txt`.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py` from this directory. With empty inventory or `NETMIKO_USE_MOCK=1`, it uses mock and prints fixture output.
4. Compare with `solution.py`.

## Prerequisites

- **netmiko** installed (`pip install netmiko`).
- For real device run: a reachable device and credentials (NET_USER, NET_PASS env vars).

## Mock Mode

Set `NETMIKO_USE_MOCK=1` or keep `minimal/devices.yaml` with empty `devices: []` to run without any network devices. The mock returns the fixture file content.
