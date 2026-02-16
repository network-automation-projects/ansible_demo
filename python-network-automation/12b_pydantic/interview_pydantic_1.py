"""
Pydantic interview challenge - PRACTICE (fill in the TODOs)
Device model with validation, parse from dict, serialize to dict.

Task: Implement a small Pydantic-based device model with validation, 
parsing from a dict, and serialization back to a dict.

Device model: hostname, ip, optional port (1-65535). Hostname normalized.

"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

