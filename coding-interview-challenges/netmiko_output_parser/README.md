# Netmiko Output Parser (Python)

Practice exercise for **parsing CLI output** returned by Netmiko's `send_command()`. Focus: extract structured data from unstructured Cisco IOS `show version` and `show ip interface brief` output.

## What You'll Use

- **File I/O:** Read fixture files with `Path.read_text()` or `open()`
- **Regex / line parsing:** Extract hostname, uptime, version, model, serial from `show version`
- **Column parsing:** Parse `show ip interface brief` table (interface, IP, status, protocol)
- **Data structures:** Return dict and list of dicts

## Problem

1. **parse_show_version(output: str) -> dict**  
   Extract from Cisco-style `show version` output:
   - `hostname`: from line like `"hostname uptime is ..."` (first word before "uptime")
   - `uptime`: the text after `"uptime is "` (e.g. `"5 weeks, 2 days, 3 hours, 22 minutes"`)
   - `version`: line containing `"Cisco IOS Software"` and `"Version"` (or similar)
   - `model`: from line like `"Cisco CISCO2960-24TC-L (revision R0)"` — extract the model identifier
   - `serial`: from `"Processor board ID XXXXX"`  
   Return `{"hostname": str, "uptime": str, "version": str, "model": str, "serial": str}`. Use `"Unknown"` for missing fields.

2. **parse_show_ip_int_brief(output: str) -> list[dict]**  
   Parse the table from `show ip interface brief`. Skip the header line. For each data line, extract:
   - `interface`: first column (e.g. `GigabitEthernet0/0`)
   - `ip`: second column (`192.168.1.1` or `unassigned`)
   - `status`: `up`, `down`, or `administratively down`
   - `protocol`: `up` or `down`  
   Return `[{"interface": str, "ip": str, "status": str, "protocol": str}, ...]`.

3. **main()**  
   Read `fixtures/show_version_ios.txt` and `fixtures/show_ip_int_brief_ios.txt`. Call both parsers and print the results.

## Files

- **fixtures/show_version_ios.txt** – Sample Cisco IOS `show version` output.
- **fixtures/show_ip_int_brief_ios.txt** – Sample `show ip interface brief` output.
- **exercise.py** – Skeleton with TODOs; implement the logic yourself first.
- **solution.py** – Reference solution. Run with: `python solution.py`.

## How to Practice

1. Read this README and inspect the fixture files.
2. Implement `exercise.py` (fill in the TODOs) without looking at `solution.py`.
3. Run `python exercise.py` from this directory; check parsed output.
4. Compare with `solution.py`.

## Prerequisites

- None. Standard library only; no Netmiko required.

## Example Output

```
parse_show_version: hostname=switch1, uptime=5 weeks..., version=Cisco IOS Software..., model=CISCO2960-24TC-L, serial=FCW2140L0BZ
parse_show_ip_int_brief: 4 interfaces
  GigabitEthernet0/0: 192.168.1.1 up/up
  ...
```
