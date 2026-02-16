# Netmiko/NAPALM Debug Lesson

A short lesson made of **four debug challenges** for scripts that connect to devices (e.g. with Netmiko or NAPALM), run commands, and handle output. Each challenge focuses on one common class of bug; all use **mocks** so you can run them without real devices.

## What You'll Fix

| # | Issue | Challenge | Folder |
|---|--------|-----------|--------|
| 1 | Poor exception handling → script crashes on timeout | Catch timeouts per device, record failure, don't crash | [debug_netmiko_timeout_crash/](debug_netmiko_timeout_crash/) |
| 2 | Bad parsing of "show" output | Parse tables correctly when columns have multi-word values | [debug_netmiko_bad_parsing/](debug_netmiko_bad_parsing/) |
| 3 | Race conditions in parallel device handling | Avoid shared mutable state; collect results from futures | [debug_netmiko_race_condition/](debug_netmiko_race_condition/) |
| 4 | Insecure credential handling | No hardcoded secrets; no credentials in logs or committed files | [debug_netmiko_insecure_credentials/](debug_netmiko_insecure_credentials/) |

## Suggested Order

1. **Exception handling** (timeout crash) — so one bad device doesn't kill the whole run.
2. **Parsing** — so "show" output is turned into reliable data.
3. **Concurrency** — so parallel runs don't produce wrong or inconsistent results.
4. **Credentials** — so secrets stay out of code and logs.

## Per-Challenge Format

- **README.md** — Challenge description, expected vs actual behavior, how to approach.
- **buggy_*.py** — Script with an intentional bug; run it to see the failure.
- **ANSWER.md** — Root cause, fix, and best practices (read after you try).

## Prerequisites

- Basic idea of Netmiko/NAPALM (connect, send command, get output). For build-from-scratch practice see:
  - [netmiko_connection_runner/](netmiko_connection_runner/) — connection params, command mapping, optional mock.
  - [python-network-automation 04_device_management](../python-network-automation/04_device_management/) — device management module (if in same repo).

No real devices or live network required; all challenges use mocks or fixtures.
