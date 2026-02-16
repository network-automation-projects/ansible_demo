"""
Drill 12: Write a Custom Exception Hierarchy — Reference solution.
"""


class AutomationError(Exception):
    """Base exception for automation failures."""

    pass


class ValidationError(AutomationError):
    """Raised when input or config is invalid."""

    pass


class ExecutionError(AutomationError):
    """Raised when runtime execution fails (e.g. device unreachable)."""

    pass


def validate_config(config: dict) -> None:
    """Validate config. Raise ValidationError if invalid."""
    if "host" not in config:
        raise ValidationError("Missing host")


def run_task(config: dict) -> str:
    """Run task. Raise ExecutionError on failure."""
    raise ExecutionError("Device unreachable")


def main() -> None:
    try:
        validate_config({})
    except ValidationError as e:
        print("Caught:", e)
    try:
        run_task({"host": "x"})
    except ExecutionError as e:
        print("Caught:", e)


if __name__ == "__main__":
    main()
