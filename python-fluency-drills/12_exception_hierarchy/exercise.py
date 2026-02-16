"""
Drill 12: Write a Custom Exception Hierarchy
Fill in the TODOs. See README.md for the problem description.
"""


class AutomationError(Exception):
    """Base for automation failures."""

    pass


class ValidationError(AutomationError):
    """Invalid input/config."""

    pass


class ExecutionError(AutomationError):
    """Runtime failure."""

    pass


def validate_config(config: dict) -> None:
    """Validate config. Raise ValidationError if invalid."""
    # TODO: if "host" not in config: raise ValidationError("Missing host")
    raise NotImplementedError("Implement me")


def run_task(config: dict) -> str:
    """Run task. Raise ExecutionError on failure."""
    # TODO: Simulate: raise ExecutionError("Device unreachable")
    raise NotImplementedError("Implement me")


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
