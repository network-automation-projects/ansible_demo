# Answer: Where Credentials Are Exposed and How to Fix

## Root Cause

Credentials are exposed in three ways:

1. **Hardcoded defaults:** `DEFAULT_USER` and `DEFAULT_PASS` are literal secrets in source code. Anyone with repo access sees them; they may be committed to version control.
2. **Credentials in a committed file:** `load_devices(config_path)` loads YAML that may contain `username` and `password`. If `devices.yaml` is committed with real credentials, they live in the repo. The plan says "or reads from a committed config file."
3. **Logging params including password:** `logger.info("Connecting with params: %s", params)` logs the full `params` dict, which includes `password`. Logs are often stored, forwarded, or visible to more people than intended; secrets in logs are a common leak.

## Fixes

### 1. Remove hardcoded credentials; use environment variables

Use environment variables (or a secure secret store) and do not fall back to a literal password:

```python
import os

def build_connection_params(device: dict) -> dict:
    username = device.get("username") or os.environ.get("NET_USER", "")
    password = device.get("password") or os.environ.get("NET_PASS", "")
    if not password:
        raise ValueError("Password required: set NET_PASS or provide in device config (from a secure source)")
    params = {
        "host": device.get("host") or device.get("ip"),
        "device_type": device.get("device_type", "cisco_ios"),
        "username": username,
        "password": password,
    }
    # Do not log params; see below.
    return params
```

Optionally use `getpass.getpass()` for interactive prompts instead of env vars when running from a terminal.

### 2. Do not commit credentials in YAML

- Keep `devices.yaml` as a **sample** with no real secrets (e.g. `username: null`, `password: null` or placeholders), and document that real credentials come from env vars or a separate, non-committed file.
- Add `devices.yaml` to `.gitignore` if it is ever used to hold real secrets, or use a path outside the repo (e.g. `os.environ.get("DEVICES_FILE")`) for production.
- In code, prefer reading only non-secret fields (host, device_type) from the file and filling username/password from env or `getpass`.

### 3. Never log secrets

Do not log `params` or any dict that contains `password` or `secret`:

```python
logger.info("Connecting to %s as %s", params["host"], params["username"])
```

If you need to log for debugging, redact: e.g. build a copy of params with `password="***"` and log that, or use a helper that strips known secret keys before logging.

## How to Spot Similar Bugs

- **Literal passwords or tokens in code:** Search for `password =`, `secret =`, `api_key =` and similar. They should point to env vars, `getpass`, or a secure backend.
- **Logging of request/connection objects:** Any `log.info(..., params)`, `log.debug(..., kwargs)` or similar may include secrets. Log only host, username (if safe), or redacted data.
- **Config files in the repo:** If the app loads credentials from a file, check whether that file is committed and whether it contains real secrets. Prefer samples only; real config should be gitignored or outside the repo.

## Best Practices

1. **Never hardcode secrets:** Use `os.environ.get("NET_PASS")`, `getpass.getpass()`, or a vault/secret manager. Fail fast if required secrets are missing.
2. **Do not log secrets:** Avoid logging connection params, request bodies, or config that might contain passwords. Log host, user, and redacted or structural info only.
3. **Keep secrets out of version control:** Use `.env` (and add to `.gitignore`) or env vars set at runtime. Provide `.env.example` or sample config with placeholders only.
4. **Document where credentials come from:** In README or comments, state that `NET_USER`/`NET_PASS` (or similar) must be set, or that `devices.yaml` is a sample and real credentials are supplied elsewhere.
