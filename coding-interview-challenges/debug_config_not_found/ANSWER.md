# Answer: Why Config File Is Not Found When Run From Different Directory

## Root Cause

The script uses a **relative path** `"config.json"` without anchoring it to the script's location. `open("config.json")` resolves the path relative to the **current working directory** (cwd), not the directory containing the script. When you run from the project root, cwd is the project root, so Python looks for `config.json` there and fails.

## Why It Manifests

1. Run from challenge dir: `cd debug_config_not_found && python buggy_loader.py` — cwd is `debug_config_not_found`, so `config.json` is found.
2. Run from project root: `python debug_config_not_found/buggy_loader.py` — cwd is the project root. Python looks for `config.json` in the project root; it's actually in `debug_config_not_found/`. FileNotFoundError.
3. In CI/CD, the workspace root is often the repo root. Scripts that assume cwd == script dir will break.

## Code Fix

Resolve the config path relative to the script file using `__file__`:

```python
from pathlib import Path

def load_config(config_path: str | None = None) -> dict:
    if config_path is None:
        script_dir = Path(__file__).resolve().parent
        config_path = script_dir / "config.json"
    with open(config_path) as f:
        return json.load(f)
```

Or, when calling from `main()`:

```python
def main() -> None:
    script_dir = Path(__file__).resolve().parent
    config_path = script_dir / "config.json"
    config = load_config(str(config_path))
    ...
```

## How to Spot Similar Bugs

- **Relative paths in scripts:** Any `open("file.txt")` or `Path("data/")` that doesn't use `__file__` is cwd-dependent.
- **"Works on my machine":** Often means the developer always runs from a specific directory. CI or other users may run from elsewhere.
- **Path operations:** Check whether paths are built from `os.getcwd()` (cwd) vs `Path(__file__).parent` (script dir).

## Best Practices

1. **Anchor to script or package:** Use `Path(__file__).resolve().parent` for paths next to the script. For packages, use `importlib.resources` or `pkg_resources`.
2. **Explicit base path:** Accept a base directory or config path as an argument or env var for flexibility.
3. **Document cwd requirements:** If a script must be run from a specific directory, document it clearly and consider failing fast with a helpful message if config is missing.
