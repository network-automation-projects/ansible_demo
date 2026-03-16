# Ready-to-use config snippets.
# Never hardcode secrets. Use env vars or pydantic-settings. See python-from-basic-to-tools.md

import os

# -----------------------------------------------------------------------------
# Simple env var — os.environ.get with optional default
# -----------------------------------------------------------------------------

# api_key = os.environ.get("API_KEY")
# if not api_key:
#     raise ValueError("API_KEY environment variable required")

# With default:
# debug = os.environ.get("DEBUG", "false").lower() == "true"
# port = int(os.environ.get("PORT", "8080"))

# -----------------------------------------------------------------------------
# pydantic-settings — typed config with validation and .env loading
# Requires: pip install pydantic-settings
# -----------------------------------------------------------------------------

# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     api_key: str
#     debug: bool = False
#     port: int = 8080
#
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"
#
#
# settings = Settings()
# # settings.api_key  # from env or .env
# # settings.debug
# # settings.port
