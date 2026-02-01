"""
Exercise: parse .env-style file into dict; skip comments and blanks.
Fill in the TODOs. See README.md for the problem description.
"""

from pathlib import Path


def load_env(path: str) -> dict[str, str]:
    """Read .env-style file; return dict of KEY=value. Skip comments (#) and blank lines."""
    result = {}
    # TODO: open path, loop over lines
    # TODO: strip line; if empty or startswith("#"), continue
    # TODO: split on first "=" only (e.g. line.split("=", 1)); strip key and value; result[key] = value
    # TODO: handle FileNotFoundError: print message and return {}
    return result


def main() -> None:
    base = Path(__file__).parent
    path = base / ".env.example"
    env = load_env(str(path))
    for k, v in sorted(env.items()):
        print(f"{k}={v}")


if __name__ == "__main__":
    main()
