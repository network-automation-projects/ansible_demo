"""
defaultdict and Related Patterns — Exercises
=============================================

Practice using collections.defaultdict for grouping, counting, and aggregating
data without manual key checks. Useful for automation scripts and AI/LLM
integration (e.g. grouping API responses, building context buckets for RAG).

Prerequisites: Module 01 (Core Fundamentals). Use with: exercises.py (other collections).
"""

from collections import defaultdict

# --- defaultdict basics ---
# defaultdict(factory) creates a dict that auto-creates a value for missing keys
# using the factory (e.g. list, int, set). No more "if key not in d: d[key] = []".
#
# Example: d = defaultdict(list); d["a"].append(1)  # "a" did not exist; now d["a"] == [1]
# TODO: Create a defaultdict that defaults to int. Assign d["x"] = 10 and print d["y"]
# (y was never set — what value do you get?). Then print the whole dict.

d = defaultdict(int, 10)   # your code here
d["x"] = 10
print(d["y"])
print(dict(d))


# --- grouping with defaultdict(list) ---
# Very common in automation: group items by a key (e.g. interfaces by status, devices by site).
# With a normal dict you must do: if key not in result: result[key] = []; result[key].append(item)
# With defaultdict(list): result[key].append(item) is enough.
#
# Interfaces: list of dicts with "name" and "status". Group interface names by status.
# Expected: {"up": ["Eth0", "Eth2"], "down": ["Eth1"]}

interfaces = [
    {"name": "Eth0", "status": "up"},
    {"name": "Eth1", "status": "down"},
    {"name": "Eth2", "status": "up"},
]

# grouped = defaultdict(list)
# for iface in interfaces:
#     # append iface["name"] under key iface["status"]
#     ...
# print(dict(grouped))


# --- manual dict vs defaultdict ---
# Same grouping with a normal dict (no defaultdict). Use .get(key, []) and reassign
# so that you append to a list that might not exist yet.
# Group the same interfaces by status into a plain dict "manual_grouped".

# manual_grouped = {}
# for iface in interfaces:
#     status = iface["status"]
#     # get current list or [], append name, store back
#     ...
# print(manual_grouped)


# --- defaultdict(int) — simple counts ---
# Default 0 for missing keys. Great for histograms, word counts, error-type counts.
# Count how many times each status appears in the interfaces list above.
# Expected: {"up": 2, "down": 1}

# status_counts = defaultdict(int)
# for iface in interfaces:
#     ...
# print(dict(status_counts))


# --- defaultdict(set) — unique items per key ---
# Use when each key should map to a set of unique values (e.g. which devices have which VLANs).
# Given: devices_reporting_vlan = [("r1", "10"), ("r2", "10"), ("r1", "20"), ("r3", "10")]
# Build a dict: vlan -> set of device names. So "10" -> {"r1", "r2", "r3"}, "20" -> {"r1"}.

devices_reporting_vlan = [("r1", "10"), ("r2", "10"), ("r1", "20"), ("r3", "10")]

# vlan_to_devices = defaultdict(set)
# for device, vlan in devices_reporting_vlan:
#     ...
# print({k: sorted(v) for k, v in vlan_to_devices.items()})


# --- automation: group devices by site ---
# Common in automation: list of device dicts with "hostname" and "site".
# Group hostnames by site using defaultdict(list). Return a normal dict (dict(grouped)).

devices = [
    {"hostname": "r1", "site": "NYC"},
    {"hostname": "r2", "site": "NYC"},
    {"hostname": "sw1", "site": "LA"},
]

# def devices_by_site(devices_list):
#     grouped = defaultdict(list)
#     for d in devices_list:
#         ...
#     return dict(grouped)
# print(devices_by_site(devices))


# --- AI / LLM integration: group responses by category ---
# When calling an LLM or API per item, you often get back a "category" or "label".
# Group the raw responses (or IDs) by that category for later use (e.g. batching, RAG buckets).
# Simulated API responses: list of dicts with "id" and "category". Group ids by category.

api_responses = [
    {"id": "resp_1", "category": "network"},
    {"id": "resp_2", "category": "security"},
    {"id": "resp_3", "category": "network"},
]

# by_category = defaultdict(list)
# for r in api_responses:
#     ...
# print(dict(by_category))


# --- optional: custom default with lambda ---
# Sometimes you want a default that is not list/set/int. Example: default to {"count": 0, "items": []}.
# d = defaultdict(lambda: {"count": 0, "items": []})
# d["a"]["count"] += 1
# d["a"]["items"].append("first")
# TODO: Create such a defaultdict, add one key "test" with count 2 and items ["x", "y"], then print d["test"] and d["other"].

# custom = defaultdict(lambda: {"count": 0, "items": []})
# ...
# print(custom["test"])
# print(custom["other"])
