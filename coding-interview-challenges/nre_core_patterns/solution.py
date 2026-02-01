"""
NRE core patterns: group by role, validate, set diff, drift, batch apply.
Reference solution with inline comments: what each part does, why types, where vars are used.
"""

from typing import Any, Callable, TypeVar

# TypeVar("T") = generic type for batch_apply's apply_fn return; we don't use the return value, just need to type the callable.
T = TypeVar("T")


def group_devices_by_role(devices: list[dict]) -> dict[str, list[str]]:
    """Return a dict mapping role -> list of hostnames. Assume each dict has 'hostname' and 'role'."""
    # result is dict[str, list[str]]: keys are role names (str), values are lists of hostnames (list[str]).
    # Used as the return value; we build it by appending hostnames to the list for each role.
    result: dict[str, list[str]] = {}
    for d in devices:
        # d is one device dict; .get() returns None if key missing (defensive). role/hostname used to build result.
        role = d.get("role")
        hostname = d.get("hostname")
        # Skip devices that don't have both keys (e.g. malformed data); only then do we add to result.
        if role is not None and hostname is not None:
            # First device for this role: create the list; later we only append. result[role] used on next line.
            if role not in result:  #? what does this do? it checks if the role is in the result dictionary
                result[role] = [] #why? because if it's the first time through, there is nothing in result?
            result[role].append(hostname)
    return result


def filter_valid_devices(devices: Any) -> list[dict]:
    """Return only dicts that have 'hostname' and 'ip' as non-empty strings. Raise ValueError if not a list."""
    # Input validation first: devices must be a list. We raise so the caller gets a clear error (defensive).
    if not isinstance(devices, list):
        raise ValueError("devices must be a list")
    # List comprehension: we build a new list of dicts. d is each item; we keep d only if it's a dict with both keys.
    # d.get("hostname") and d.get("ip") are truthy only when non-empty strings (empty string "" is falsy).
    return [
        d
        for d in devices
        if isinstance(d, dict)
        and d.get("hostname")
        and d.get("ip")
    ]


def device_set_diff(
    expected: list[str] | set[str],
    discovered: list[str] | set[str],
) -> tuple[set[str], set[str]]:
    """Return (missing, extra): expected - discovered, discovered - expected."""
    # exp, disc are sets so we can use set subtraction. set() works on both list and set input.
    # exp is used in (exp - disc); disc is used in (disc - exp). Returned as (missing, extra).
    exp = set(expected)
    disc = set(discovered)
    return (exp - disc, disc - exp)


def config_drift(
    desired: dict[str, str],
    actual: dict[str, str],
) -> tuple[list[str], list[str], list[str]]:
    """Return (missing, extra, different): keys only in desired, only in actual, in both with different value."""
    # missing: list[str] — keys we want but don't have. set(desired) - set(actual); sorted so output order is stable.
    missing = sorted(set(desired) - set(actual))
    # extra: list[str] — keys we have but didn't want. set(actual) - set(desired); used in return.
    extra = sorted(set(actual) - set(desired))
    # different: list[str] — keys in both dicts but with different values. set(desired) & set(actual) = intersection.
    # desired[k] != actual[k] filters to only keys where values differ. Used in return.
    different = sorted(
        k for k in set(desired) & set(actual) if desired[k] != actual[k]
    )
    return (missing, extra, different)


def batch_apply(
    hostnames: list[str],
    apply_fn: Callable[[str], T],
) -> dict[str, list]:
    """Call apply_fn(host) for each host; return {"ok": [hosts], "failed": [(host, str(e)), ...]}."""
    # ok: list[str] — hostnames that succeeded; we append(host) on success. Returned under key "ok".
    ok: list[str] = []
    # failed: list[tuple[str, str]] — (hostname, error_message) for each failure; we append on exception. Returned under "failed".
    failed: list[tuple[str, str]] = []
    for host in hostnames:
        try:
            apply_fn(host)
            ok.append(host)
        except Exception as e:
            # str(e) so we store a string message, not the exception object. (host, str(e)) goes into failed.
            failed.append((host, str(e)))
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
        assert "must be a list" in str(e)

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
