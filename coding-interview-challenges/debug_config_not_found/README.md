# Debug: Config File Not Found (Works From Script Dir, Fails From Project Root)

Debugging challenge for **automation-style** interviews. Focus: relative paths and working directory.

## Challenge

An automation script loads `config.yaml` from its directory. It works when you run it from inside the challenge folder (`python debug_config_not_found/buggy_loader.py` or `cd debug_config_not_found && python buggy_loader.py`). But when you run it from the project root with `python coding-interview-challenges/debug_config_not_found/buggy_loader.py`, it fails with **FileNotFoundError: config.yaml**.

**Your task:** Figure out why the script is sensitive to the current working directory and fix it.

## What You Have

- **buggy_loader.py** — Loads `config.yaml` and prints the contents.
- **config.json** — Sample config file (in the same folder as the script).
- Run from the challenge dir: `cd debug_config_not_found && python buggy_loader.py` — works.
- Run from project root: `python debug_config_not_found/buggy_loader.py` — fails (when cwd is project root).

## Expected vs Actual Behavior

- **Expected:** The script finds `config.yaml` regardless of where you run it from (script dir, project root, CI workspace, etc.).
- **Actual:** It only works when the current working directory is the script's directory.

## How to Approach

1. Run from the challenge directory — confirm it works.
2. Run from the parent directory (or project root) — observe the failure.
3. Find where the script resolves the config path. What does it use as the base?
4. Fix it so the path is relative to the script file, not the current working directory.
5. Verify: run from both locations; both should succeed.

## Files

- **buggy_loader.py** — Code to debug
- **config.json** — Sample config
- **ANSWER.md** — Full explanation (read after attempting)
