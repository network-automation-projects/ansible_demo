"""
Env parser: read .env-style file into dict; skip comments and blanks.
"""

from pathlib import Path


def load_env(path: str) -> dict[str, str]:
    """Read .env-style file; return dict of KEY=value. Skip comments (#) and blank lines."""
    result: dict[str, str] = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if key:
                    result[key] = value
    except FileNotFoundError:
        print(f"File not found: {path}")
        return {}
    return result


def main() -> None:
    base = Path(__file__).parent
    path = base / ".env.example"
    env = load_env(str(path))
    for k, v in sorted(env.items()):
        print(f"{k}={v}")


if __name__ == "__main__":
    main()
