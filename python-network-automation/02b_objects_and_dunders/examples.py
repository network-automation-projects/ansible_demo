"""
Python Network Automation - Objects and Dunders Examples
=========================================================

Complete working examples demonstrating special methods (dunders)
in network automation types.
"""

from typing import Any, Dict, Iterator, List, Optional, Union
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Device with __repr__, __str__, and __eq__
# ============================================================================


class Device:
    """
    Network device with clear representation and value equality.

    __repr__: unambiguous, ideally looks like a constructor call (for debugging).
    __str__: human-friendly (for logs and reports).
    __eq__: two devices are equal if hostname and vendor match.
    """

    def __init__(self, hostname: str, vendor: str, ip: Optional[str] = None) -> None:
        self.hostname = hostname
        self.vendor = vendor
        self.ip = ip

    def __repr__(self) -> str:
        return f"Device(hostname={self.hostname!r}, vendor={self.vendor!r}, ip={self.ip!r})"

    def __str__(self) -> str:
        return f"{self.hostname} ({self.vendor})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Device):
            return NotImplemented
        return self.hostname == other.hostname and self.vendor == other.vendor


# ============================================================================
# Example 2: Device list with __len__, __getitem__, __iter__, __contains__
# ============================================================================


class DeviceList:
    """
    Wrapper around a list of devices that supports len(), indexing, iteration, and 'in'.

    __len__: len(device_list) returns number of devices.
    __getitem__: device_list[0] or device_list['r1'] by hostname.
    __iter__: for device in device_list works.
    __contains__: device in device_list or 'r1' in device_list by hostname.
    """

    def __init__(self, devices: Optional[List[Device]] = None) -> None:
        self._devices: List[Device] = list(devices) if devices else []

    def __len__(self) -> int:
        return len(self._devices)

    def __getitem__(self, key: Union[int, str]) -> Device:
        if isinstance(key, int):
            return self._devices[key]
        for d in self._devices:
            if d.hostname == key:
                return d
        raise KeyError(key)

    def __iter__(self) -> Iterator[Device]:
        return iter(self._devices)

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, Device):
            return item in self._devices
        if isinstance(item, str):
            return any(d.hostname == item for d in self._devices)
        return False


# ============================================================================
# Example 3: Callable runner (__call__)
# ============================================================================


class RetryRunner:
    """
    Object that is callable: runner(cmd) runs the command with retries.

    __call__: when you do runner(cmd), Python invokes __call__(runner, cmd).
    """

    def __init__(self, max_attempts: int = 3) -> None:
        self.max_attempts = max_attempts

    def __call__(self, command: str) -> str:
        """Run command (simulated); in real code this would run on a device."""
        logger.info("RetryRunner.__call__ invoked with command=%s", command)
        return f"result of: {command}"


# ============================================================================
# Example 4: Context manager (__enter__, __exit__)
# ============================================================================


class ConnectionContext:
    """
    Simulated connection context: with block handles connect/disconnect.

    __enter__: called when entering 'with'; return value is bound to 'as' variable.
    __exit__: called when leaving 'with' (normal or exception); cleanup here.
    """

    def __init__(self, hostname: str) -> None:
        self.hostname = hostname
        self._connected = False

    def __enter__(self) -> "ConnectionContext":
        logger.info("Connecting to %s", self.hostname)
        self._connected = True
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> bool:
        logger.info("Disconnecting from %s", self.hostname)
        self._connected = False
        return False  # do not suppress exceptions


# ============================================================================
# Demo: using the examples
# ============================================================================


def demo_device_representation() -> None:
    """Show __repr__ vs __str__ and __eq__."""
    r1 = Device("r1", "cisco", "10.0.0.1")
    r2 = Device("r1", "cisco")
    r3 = Device("r2", "juniper")

    logger.info("repr(r1) = %s", repr(r1))
    logger.info("str(r1) = %s", str(r1))
    logger.info("r1 == r2 (same hostname/vendor): %s", r1 == r2)
    logger.info("r1 == r3: %s", r1 == r3)


def demo_device_list_protocol() -> None:
    """Show __len__, __getitem__, __iter__, __contains__."""
    devices = DeviceList(
        [Device("r1", "cisco"), Device("r2", "juniper"), Device("sw1", "arista")]
    )

    logger.info("len(devices) = %s", len(devices))
    logger.info("devices[0] = %s", devices[0])
    logger.info("devices['r2'] = %s", devices["r2"])
    logger.info("'sw1' in devices: %s", "sw1" in devices)
    for d in devices:
        logger.info("  %s", d)


def demo_callable_and_context() -> None:
    """Show __call__ and with block."""
    runner = RetryRunner(max_attempts=3)
    result = runner("show version")
    logger.info("runner('show version') -> %s", result)

    with ConnectionContext("r1") as conn:
        logger.info("Inside with block, conn.hostname = %s", conn.hostname)
    logger.info("Exited with block")


if __name__ == "__main__":
    demo_device_representation()
    demo_device_list_protocol()
    demo_callable_and_context()
