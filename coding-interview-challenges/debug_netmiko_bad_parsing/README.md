# Debug: Wrong Interface Status from "show ip interface brief" Parser

Debugging challenge for **parsing CLI output** (e.g. from Netmiko's `send_command`). Focus: fragile parsing that breaks on real IOS output.

## Challenge

A script parses Cisco IOS `show ip interface brief` output and extracts interface, IP, status, and protocol. For some lines the parsed **status** or **protocol** is wrong (e.g. "administratively" instead of "administratively down", or status and protocol swapped).

**Your task:** Find why the parser produces incorrect status/protocol for interfaces that are "administratively down", and fix it.

## What You Have

- **buggy_parser.py** — Reads the fixture and parses each data line. Prints the parsed table.
- **fixtures/show_ip_int_brief_ios.txt** — Sample Cisco IOS output (header + 4 interface lines).
- Run: `python buggy_parser.py`

## Expected vs Actual Behavior

- **Expected:** Each row has correct status and protocol. For example:
  - `GigabitEthernet0/2`: status `administratively down`, protocol `down`
  - `Vlan1`: status `administratively down`, protocol `down`
- **Actual:** For interfaces with "administratively down", status is wrong (e.g. "administratively" only, or "down" in the wrong column) and/or protocol is wrong.

## How to Approach

1. Run the script and inspect the printed table.
2. Compare with the raw fixture: which lines have two-word status ("administratively down")?
3. Look at how the parser splits or indexes columns. Why does it break for those lines?
4. Fix the parsing so status and protocol are correct for all rows.
5. Verify: re-run and check GigabitEthernet0/2 and Vlan1.

## Files

- **buggy_parser.py** — Code to debug
- **fixtures/show_ip_int_brief_ios.txt** — Sample CLI output
- **ANSWER.md** — Full explanation (read after attempting)
