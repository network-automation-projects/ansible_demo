"""
Exercise: load key=value configs, merge (second wins), optionally diff.
Fill in the TODOs. See README.md for the problem description.
"""

from pathlib import Path


def load_config(path: str) -> dict[str, str]:
    """Read key=value file; return dict. Skip comments (#) and blank lines."""
    result = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip()
                if key:
                    result[key] = value
    except FileNotFoundError:
        print(f"File not found: {path}")
        return {}
    return result


def merge_configs(first: dict[str, str], second: dict[str, str]) -> dict[str, str]:
    """Merge second into first; second wins for overlapping keys. Return new dict."""
    result = dict(first)
    result.update(second)
    return result


def config_diff(
    a: dict[str, str], b: dict[str, str]
) -> tuple[set[str], set[str], set[str]]:
    """Return (only_in_a, only_in_b, keys_in_both_with_different_value)."""
    only_a = set(a) - set(b)
    only_b = set(b) - set(a)
    different = {k for k in set(a) & set(b) if a[k] != b[k]}
    return (only_a, only_b, different)


def main() -> None:
    base = Path(__file__).parent
    path_a = base / "config_a.txt"
    path_b = base / "config_b.txt"
    cfg_a = load_config(str(path_a))
    cfg_b = load_config(str(path_b))
    merged = merge_configs(cfg_a, cfg_b)
    print("Merged:", merged)
    only_a, only_b, different = config_diff(cfg_a, cfg_b)
    print("Only in A:", only_a)
    print("Only in B:", only_b)
    print("Different:", different)


if __name__ == "__main__":
    main()
