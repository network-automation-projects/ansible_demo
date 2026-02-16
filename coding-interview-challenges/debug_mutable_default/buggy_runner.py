"""
Buggy batch processor for devices.

When run twice with different device lists, the second run includes
devices from the first run. Why?
"""


def process_batch(devices: list[str], results: list[str] = []) -> list[str]:
    """
    Process each device and return a list of processed hostnames.
    Simulated: just appends each device name to results.
    """
    for device in devices:
        results.append(device)
    return results


def main() -> None:
    batch1 = process_batch(["router-1", "router-2"])
    print("Batch 1:", batch1)

    batch2 = process_batch(["core-sw1", "core-sw2"])
    print("Batch 2:", batch2)

    # Expected: Batch 2 should be ["core-sw1", "core-sw2"] only
    assert batch2 == ["core-sw1", "core-sw2"], f"Unexpected: {batch2}"


if __name__ == "__main__":
    main()
