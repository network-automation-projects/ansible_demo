"""
defaultdict and Related Patterns — Solutions
=============================================

Full solutions with comments. Run this file to see output after trying
exercises_defaultdict_1.py.
"""

from collections import defaultdict

# --- defaultdict basics ---
# Missing keys get a new value from the factory (list -> [], int -> 0, set -> set()).
# So d["y"] never set -> defaultdict calls int() -> 0.

d = defaultdict(int)
d["x"] = 10
print(d["y"])   # 0 (key "y" did not exist; int() gives 0)
print(dict(d))  # {'x': 10, 'y': 0} — "y" was auto-created when we read it


# --- grouping with defaultdict(list) ---
# No "if status not in grouped" needed; first access to grouped[status] creates [].

interfaces = [
    {"name": "Eth0", "status": "up"},
    {"name": "Eth1", "status": "down"},
    {"name": "Eth2", "status": "up"},
]

grouped = defaultdict(list)
for iface in interfaces:
    grouped[iface["status"]].append(iface["name"])
print(dict(grouped))  # {'up': ['Eth0', 'Eth2'], 'down': ['Eth1']}


# --- manual dict vs defaultdict ---
# With a normal dict you must ensure the list exists before appending.
# Get current list (or [] for new key), append, then store back.

manual_grouped = {}
for iface in interfaces:
    status = iface["status"]
    current = manual_grouped.get(status, [])        # get the list of the current items associated with that status in the dictionary so far or empty list
    current.append(iface["name"])                   # append new interface name to that list
    manual_grouped[status] = current                # add that list as a value to that status key in the grouped dictionary
# Alternative: manual_grouped.setdefault(status, []).append(iface["name"])
print(manual_grouped)  # same as grouped


# --- defaultdict(int) — simple counts ---
# Every missing key gets 0; += 1 then works without checking.

status_counts = defaultdict(int)
for iface in interfaces:
    status_counts[iface["status"]] += 1
print(dict(status_counts))  # {'up': 2, 'down': 1}


# --- defaultdict(set) — unique items per key ---
# Each vlan maps to a set of devices; duplicates are automatically ignored.

devices_reporting_vlan = [("r1", "10"), ("r2", "10"), ("r1", "20"), ("r3", "10")]

vlan_to_devices = defaultdict(set)
for device, vlan in devices_reporting_vlan:
    vlan_to_devices[vlan].add(device)
print({k: sorted(v) for k, v in vlan_to_devices.items()})
# {'10': ['r1', 'r2', 'r3'], '20': ['r1']}


# --- automation: group devices by site ---
# Typical automation pattern: one loop, no key checks. Return dict() if callers
# expect a plain dict (e.g. for JSON serialization or to avoid accidental new keys later).

devices = [
    {"hostname": "r1", "site": "NYC"},
    {"hostname": "r2", "site": "NYC"},
    {"hostname": "sw1", "site": "LA"},
]


def devices_by_site(devices_list):
    grouped = defaultdict(list)
    for d in devices_list:
        grouped[d["site"]].append(d["hostname"])
    return dict(grouped)


print(devices_by_site(devices))  # {'NYC': ['r1', 'r2'], 'LA': ['sw1']}


# --- AI / LLM integration: group responses by category ---
# After calling an API or LLM per item, grouping by category lets you batch
# follow-up calls, build RAG buckets, or aggregate by label.

api_responses = [
    {"id": "resp_1", "category": "network"},
    {"id": "resp_2", "category": "security"},
    {"id": "resp_3", "category": "network"},
]

by_category = defaultdict(list)
for r in api_responses:
    by_category[r["category"]].append(r["id"])
print(dict(by_category))  # {'network': ['resp_1', 'resp_3'], 'security': ['resp_2']}


# --- optional: custom default with lambda ---
# lambda returns a new dict each time a missing key is accessed. Use for
# nested structures (e.g. per-key stats with count + items).

custom = defaultdict(lambda: {"count": 0, "items": []})
custom["test"]["count"] += 2
custom["test"]["items"].append("x")
custom["test"]["items"].append("y")
print(custom["test"])   # {'count': 2, 'items': ['x', 'y']}
print(custom["other"])  # {'count': 0, 'items': []} — new key gets fresh dict
