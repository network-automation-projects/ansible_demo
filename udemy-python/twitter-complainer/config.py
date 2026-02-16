"""
Env-based config for Internet Speed X Complainer bot.
Load .env via python-dotenv when available (local dev).
Secrets: X_EMAIL, X_PASSWORD — never hardcode or commit.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

# Promised speeds (Mbps) — optional defaults
PROMISED_DOWN = int(os.environ.get("PROMISED_DOWN", "150"))
PROMISED_UP = int(os.environ.get("PROMISED_UP", "10"))

# ChromeDriver: set CHROME_DRIVER_PATH or leave unset to use webdriver-manager
CHROME_DRIVER_PATH: str | None = os.environ.get("CHROME_DRIVER_PATH") or None

# X credentials — from env only (no defaults)
X_EMAIL = os.environ.get("X_EMAIL", "").strip()
X_PASSWORD = os.environ.get("X_PASSWORD", "").strip()


def require_x_credentials() -> None:
    """Raise if X_EMAIL or X_PASSWORD are missing."""
    if not X_EMAIL or not X_PASSWORD:
        raise ValueError(
            "Set X_EMAIL and X_PASSWORD in the environment (or .env). "
            "Do not commit credentials."
        )
