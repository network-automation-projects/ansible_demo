# Debug: Insecure Credential Handling

Debugging/code-review challenge for **Netmiko/NAPALM-style** automation. Focus: finding and fixing credential exposure.

## Challenge

A device runner builds connection parameters and connects to a list of devices. The code **exposes credentials** in more than one way: hardcoded values, credentials in a file that could be committed, or logging that includes secrets.

**Your task:** Review the code, find every place credentials are exposed or handled unsafely, and fix them (use environment variables, avoid logging secrets, etc.). No real connections; code review only.

## What You Have

- **buggy_runner.py** — Builds device params and runs a mock connection. Contains intentional credential-handling mistakes.
- Run: `python buggy_runner.py` (optional; mock only, no real SSH). Focus on reading the code.

## Expected vs Actual Behavior

- **Expected:** No passwords or secrets in source code or in log output. Credentials come from environment variables or secure input (e.g. `getpass`). Config files with secrets are not loaded from the repo or are clearly excluded (e.g. in `.gitignore`).
- **Actual:** Passwords are hardcoded, or connection params are logged (including password), or a credentials file is loaded from the repo.

## How to Approach

1. Read `buggy_runner.py` from top to bottom.
2. Look for: literal passwords, usernames or passwords in log messages, YAML/JSON/config that could be committed with secrets, and any path that would send secrets to the console or logs.
3. List each issue and fix it: use `os.environ.get("NET_USER")` / `NET_PASS`, remove secrets from logs, stop loading credentials from a committed file (or use a sample file and document that real credentials live elsewhere).
4. Verify: no secrets in code or in normal log output.

## Files

- **buggy_runner.py** — Code to review and fix
- **ANSWER.md** — Full explanation (read after attempting)
