"""
Config merge: load key=value configs, merge (second wins), diff.
"""

from pathlib import Path


def load_config(path: str) -> dict[str, str]:
    """Read key=value file; return dict. Skip comments (#) and blank lines."""
    result: dict[str, str] = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=") #partition is a method that splits the string into a tuple of three parts, the _ is where the = is located
                key = key.strip()
                value = value.strip()
                if key: #when would there not be a key? if the line is empty or a comment
                    result[key] = value
    except FileNotFoundError:
        print(f"File not found: {path}")
        return {}
    return result


def merge_configs(first: dict[str, str], second: dict[str, str]) -> dict[str, str]:
    """Merge second into first; second wins for overlapping keys. Return new dict."""
    result = dict(first)
    result.update(second)  #so update is a method that updates the dictionary with the keys and values from the second dictionary
    return result


def config_diff(
    a: dict[str, str], b: dict[str, str]
) -> tuple[set[str], set[str], set[str]]:
    """Return (only_in_a, only_in_b, keys_in_both_with_different_value)."""
    only_a = set(a) - set(b)
    only_b = set(b) - set(a)
    different = {k for k in set(a) & set(b) if a[k] != b[k]}     # so, you can do a set comprehension with a dictionary? yeah, you can do a set comprehension with a dictionary because a dictionary is a collection of key-value pairs
                       # a[k] is the value of the key k in the dictionary a
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
