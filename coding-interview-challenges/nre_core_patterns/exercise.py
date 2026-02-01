"""
Exercise: NRE core patterns — group by role, validate, set diff, drift, batch apply.
Fill in the TODOs below. Problem descriptions are in this file so you don't need the README open.

--------------------------------------------------------------------------------
PROBLEM DESCRIPTIONS (what you're trying to accomplish)
--------------------------------------------------------------------------------

1. group_devices_by_role(devices)
   GOAL: Build a dict that maps each "role" to a list of hostnames.
   INPUT: List of dicts; each dict has at least "hostname" and "role".
   OUTPUT: e.g. {"edge": ["e1", "e2"], "core": ["c1"]}.

2. filter_valid_devices(devices)
   GOAL: Keep only device dicts that have both "hostname" and "ip" as non-empty strings.
   RULES: If devices is not a list, raise ValueError("devices must be a list").
   OUTPUT: List of valid dicts (e.g. [{"hostname": "a", "ip": "1.2.3.4"}] only).

3. device_set_diff(expected, discovered)
   GOAL: Find which hostnames are missing from discovery and which are extra.
   RETURN: (missing, extra) where missing = expected - discovered, extra = discovered - expected.
   INPUT: Can be list or set; convert to set inside the function.

4. config_drift(desired, actual)
   GOAL: Compare two config dicts (e.g. desired state vs actual state).
   RETURN: (missing, extra, different) — keys only in desired, only in actual, or in both with different values.
   OUTPUT: Use sorted lists so order is stable.

5. batch_apply(hostnames, apply_fn)
   GOAL: Call apply_fn(host) for each host; collect successes and failures without losing state.
   RETURN: {"ok": [list of hostnames that succeeded], "failed": [(hostname, error_message), ...]}.
   On exception, append (host, str(e)) to "failed"; on success, append host to "ok".
--------------------------------------------------------------------------------
"""

from logging import raiseExceptions
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def group_devices_by_role(devices: list[dict]) -> dict[str, list[str]]:
    """Return a dict mapping role -> list of hostnames. Assume each dict has 'hostname' and 'role'."""
    result: dict[str, list[str]] = {}
                                                            # TODO: for d in devices: role = d.get("role"); hostname = d.get("hostname"); append hostname to result[role] #did we accidentally put the answer here?    
                                                            # TODO: use result[role] = result.get(role, []) + [hostname] or defaultdict(list) #defaultdict is a dictionary that will default to a list if the key is not found
    
    for d in devices:
        # get hostname
        d_hostname = d.get("hostname")
        d_role = d.get("role")

        #don't allow if the data is malformed (not there)
        if d_role is not None and d_hostname is not None:
            #append role to the list of hostnames
            #append hostname to result[role]
            #if first time through, there is nothing in result?
            if d_role not in result:
                result[d_role] = []
            result[d_role].append(d_hostname)
    
    return result


def filter_valid_devices(devices: Any) -> list[dict]:
    """Return only dicts that have 'hostname' and 'ip' as non-empty strings. Raise ValueError if not a list."""
                                                                                        # TODO: if not isinstance(devices, list): raise ValueError("devices must be a list")
                                                                                        # TODO: return [d for d in devices if isinstance(d, dict) and d.get("hostname") and d.get("ip")]
    if not isinstance(devices, list):
        raise ValueError("devices must be a list")

    return [
        d
        for d in devices
        if isinstance(d, dict) and d.get("hostname") and d.get("ip")
    ]
    

def device_set_diff(
    expected: list[str] | set[str],
    discovered: list[str] | set[str],
) -> tuple[set[str], set[str]]:
    """Return (missing, extra): expected - discovered, discovered - expected."""
                                                                    # TODO: exp = set(expected); disc = set(discovered); return (exp - disc, disc - exp)
    
    # make sure the input is a set
    expected_set = set(expected)
    discovered_set = set(discovered)

    # get the set of missing one's

    return (expected_set - discovered_set, discovered_set - expected_set)


def config_drift(
    desired: dict[str, str],
    actual: dict[str, str],
) -> tuple[list[str], list[str], list[str]]:
    """Return (missing, extra, different): keys only in desired, only in actual, in both with different value."""
    missing: list[str] = []
    extra: list[str] = []
    different: list[str] = []
                                                                    # TODO: missing = sorted(set(desired) - set(actual)); extra = sorted(set(actual) - set(desired))
                                                                    # TODO: different = sorted(k for k in set(desired) & set(actual) if desired[k] != actual[k])
    
    #find the missing one's keeping them sorted (turn them into sets)
    missing = sorted(set(desired) - set(actual))
    extra = sorted(set(actual) - set(desired))
    #if desired is there but with the wrong actual value
    different = sorted(d for d in set(desired) & set(actual) if desired[d] != actual[d])
    return (missing, extra, different)


def batch_apply(
    hostnames: list[str],
    apply_fn: Callable[[str], T],
) -> dict[str, list]:
    """Call apply_fn(host) for each host; return {"ok": [hosts], "failed": [(host, str(e)), ...]}."""
    ok: list[str] = []
    failed: list[tuple[str, str]] = []  #why use tuple here? because we want to store the hostname and the error message
                                                                    # TODO: for host in hostnames: try: apply_fn(host); ok.append(host); except Exception as e: failed.append((host, str(e)))
                                                                    # TODO: return {"ok": ok, "failed": failed}
    for h in hostnames:
        try:
            apply_fn(h)
            ok.append(h)
        except Exception as e:
            failed.append((h, str(e)))
    return {"ok": ok, "failed": failed}


def main() -> None:
    # 1. Group by role
    devices = [
        {"hostname": "e1", "role": "edge", "ip": "1.1.1.1"},
        {"hostname": "e2", "role": "edge", "ip": "1.1.1.2"},
        {"hostname": "c1", "role": "core", "ip": "2.2.2.1"},
    ]
    grouped = group_devices_by_role(devices)
    assert grouped.get("edge") == ["e1", "e2"] and grouped.get("core") == ["c1"]

    # 2. Filter valid
    raw = [{"hostname": "a", "ip": "1.2.3.4"}, {"hostname": "b"}]
    valid = filter_valid_devices(raw)
    assert len(valid) == 1 and valid[0]["hostname"] == "a"
    try:
        filter_valid_devices("not a list")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "devices must be a list" in str(e)  # incomplete why does it say devices must be a list?

    # 3. Set diff
    missing, extra = device_set_diff(["a", "b", "c"], ["a", "c", "d"])
    assert missing == {"b"} and extra == {"d"}

    # 4. Config drift
    desired = {"a": "v1", "b": "v2"}
    actual = {"a": "v1", "b": "v3", "c": "v"}
    miss, ext, diff = config_drift(desired, actual)
    assert miss == [] and set(ext) == {"c"} and set(diff) == {"b"}

    # 5. Batch apply
    def flaky(host: str) -> str:
        if host == "fail-me":
            raise ConnectionError("simulated")
        return "ok"

    result = batch_apply(["h1", "fail-me", "h2"], flaky)
    assert result["ok"] == ["h1", "h2"] and len(result["failed"]) == 1
    assert result["failed"][0][0] == "fail-me" and "simulated" in result["failed"][0][1]

    print("All assertions passed.")


if __name__ == "__main__":
    main()









# """
# Exercise: NRE core patterns — group by role, validate, set diff, drift, batch apply.
# Fill in the TODOs below. Problem descriptions are in this file so you don't need the README open.

# --------------------------------------------------------------------------------
# PROBLEM DESCRIPTIONS (what you're trying to accomplish)
# --------------------------------------------------------------------------------

# 1. group_devices_by_role(devices)
#    GOAL: Build a dict that maps each "role" to a list of hostnames.
#    INPUT: List of dicts; each dict has at least "hostname" and "role".
#    OUTPUT: e.g. {"edge": ["e1", "e2"], "core": ["c1"]}.

# 2. filter_valid_devices(devices)
#    GOAL: Keep only device dicts that have both "hostname" and "ip" as non-empty strings.
#    RULES: If devices is not a list, raise ValueError("devices must be a list").
#    OUTPUT: List of valid dicts (e.g. [{"hostname": "a", "ip": "1.2.3.4"}] only).

# 3. device_set_diff(expected, discovered)
#    GOAL: Find which hostnames are missing from discovery and which are extra.
#    RETURN: (missing, extra) where missing = expected - discovered, extra = discovered - expected.
#    INPUT: Can be list or set; convert to set inside the function.

# 4. config_drift(desired, actual)
#    GOAL: Compare two config dicts (e.g. desired state vs actual state).
#    RETURN: (missing, extra, different) — keys only in desired, only in actual, or in both with different values.
#    OUTPUT: Use sorted lists so order is stable.

# 5. batch_apply(hostnames, apply_fn)
#    GOAL: Call apply_fn(host) for each host; collect successes and failures without losing state.
#    RETURN: {"ok": [list of hostnames that succeeded], "failed": [(hostname, error_message), ...]}.
#    On exception, append (host, str(e)) to "failed"; on success, append host to "ok".
# --------------------------------------------------------------------------------
# """

# from typing import Any, Callable, TypeVar

# T = TypeVar("T")


# def group_devices_by_role(devices: list[dict]) -> dict[str, list[str]]:
#     """Return a dict mapping role -> list of hostnames. Assume each dict has 'hostname' and 'role'."""
#     result: dict[str, list[str]] = {}
#                                                             # TODO: for d in devices: role = d.get("role"); hostname = d.get("hostname"); append hostname to result[role] #did we accidentally put the answer here?    
#                                                             # TODO: use result[role] = result.get(role, []) + [hostname] or defaultdict(list) #defaultdict is a dictionary that will default to a list if the key is not found
    
#     return result


# def filter_valid_devices(devices: Any) -> list[dict]:
#     """Return only dicts that have 'hostname' and 'ip' as non-empty strings. Raise ValueError if not a list."""
#                                                                           # TODO: if not isinstance(devices, list): raise ValueError("devices must be a list")
#                                                                         # TODO: return [d for d in devices if isinstance(d, dict) and d.get("hostname") and d.get("ip")]
    
    

# def device_set_diff(
#     expected: list[str] | set[str],
#     discovered: list[str] | set[str],
# ) -> tuple[set[str], set[str]]:
#     """Return (missing, extra): expected - discovered, discovered - expected."""
#                                                                     # TODO: exp = set(expected); disc = set(discovered); return (exp - disc, disc - exp)
    
#     # make sure the input is a set
   
#     # get the set of missing one's

#     return ()


# def config_drift(
#     desired: dict[str, str],
#     actual: dict[str, str],
# ) -> tuple[list[str], list[str], list[str]]:
#     """Return (missing, extra, different): keys only in desired, only in actual, in both with different value."""
#     missing: list[str] = []
#     extra: list[str] = []
#     different: list[str] = []
#                                                                     # TODO: missing = sorted(set(desired) - set(actual)); extra = sorted(set(actual) - set(desired))
#                                                                     # TODO: different = sorted(k for k in set(desired) & set(actual) if desired[k] != actual[k])
    
#     #find the missing one's keeping them sorted (turn them into sets)
    
#     return (missing, extra, different)


# def batch_apply(
#     hostnames: list[str],
#     apply_fn: Callable[[str], T],
# ) -> dict[str, list]:
#     """Call apply_fn(host) for each host; return {"ok": [hosts], "failed": [(host, str(e)), ...]}."""
#     ok: list[str] = []
#     failed: list[tuple[str, str]] = []  #why use tuple here? because we want to store the hostname and the error message
#                                                                     # TODO: for host in hostnames: try: apply_fn(host); ok.append(host); except Exception as e: failed.append((host, str(e)))
#                                                                     # TODO: return {"ok": ok, "failed": failed}
    
  
#     return {"ok": ok, "failed": failed}


# def main() -> None:
#     # 1. Group by role
#     devices = [
#         {"hostname": "e1", "role": "edge", "ip": "1.1.1.1"},
#         {"hostname": "e2", "role": "edge", "ip": "1.1.1.2"},
#         {"hostname": "c1", "role": "core", "ip": "2.2.2.1"},
#     ]
#     grouped = group_devices_by_role(devices)
#     assert grouped.get("edge") == ["e1", "e2"] and grouped.get("core") == ["c1"]

#     # 2. Filter valid
#     raw = [{"hostname": "a", "ip": "1.2.3.4"}, {"hostname": "b"}]
#     valid = filter_valid_devices(raw)
#     assert len(valid) == 1 and valid[0]["hostname"] == "a"
#     try:
#         filter_valid_devices("not a list")
#         assert False, "expected ValueError"
#     except ValueError as e:
#         assert "devices must be a list" in str(e)  # incomplete why does it say devices must be a list?

#     # 3. Set diff
#     missing, extra = device_set_diff(["a", "b", "c"], ["a", "c", "d"])
#     assert missing == {"b"} and extra == {"d"}

#     # 4. Config drift
#     desired = {"a": "v1", "b": "v2"}
#     actual = {"a": "v1", "b": "v3", "c": "v"}
#     miss, ext, diff = config_drift(desired, actual)
#     assert miss == [] and set(ext) == {"c"} and set(diff) == {"b"}

#     # 5. Batch apply
#     def flaky(host: str) -> str:
#         if host == "fail-me":
#             raise ConnectionError("simulated")
#         return "ok"

#     result = batch_apply(["h1", "fail-me", "h2"], flaky)
#     assert result["ok"] == ["h1", "h2"] and len(result["failed"]) == 1
#     assert result["failed"][0][0] == "fail-me" and "simulated" in result["failed"][0][1]

#     print("All assertions passed.")


# if __name__ == "__main__":
#     main()
