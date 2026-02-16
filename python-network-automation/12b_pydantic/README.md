# Module 12b: Data Validation with Pydantic

Structured data validation and settings using Pydantic (beginner to advanced).

## Learning Objectives

By completing this module, you will learn:

- How to define Pydantic models with `BaseModel` and `Field()` for validation and serialization
- How to handle validation errors and serialize models to dict/JSON
- How to use nested models, validators, and optional/settings patterns
- How to load configuration from environment variables with `BaseSettings`

## Prerequisites

- Module 01: Core Fundamentals
- Module 02 or 02b (classes and types helpful)
- Basic familiarity with type hints

## Concepts Covered

### Beginner

| Concept | Description | Use in network automation |
|--------|-------------|----------------------------|
| `BaseModel` | Subclass to define a validated data structure | Device facts, API responses, config shapes |
| `Field(...)` | Required field; `Field(default=...)` for optional | hostname, ip, device_type |
| `ValidationError` | Raised when input fails validation | Catch and report invalid inventory or API data |
| `model_dump()` / `model_dump_json()` | Serialize model to dict or JSON string | Export to YAML/JSON, send to APIs |
| `model_validate(dict)` / `model_validate_json(str)` | Parse and validate from dict or JSON | Load inventory, parse API responses |

### Intermediate

| Concept | Description | Use in network automation |
|--------|-------------|----------------------------|
| Nested models | A field whose type is another `BaseModel` | Device with nested `DeviceFacts`; inventory with list of devices |
| `Field(description=..., gt=0)` | Documentation and constraints (e.g. positive int) | Port numbers, timeouts |
| `field_validator` / `model_validator` (Pydantic v2) | Custom validation logic | Normalize hostname; check IP format; cross-field checks |
| `ConfigDict` | Model config (e.g. `extra='forbid'`) | Strict parsing, optional alias handling |
| `Optional` and defaults | Optional fields, `default_factory` for mutable defaults | Optional credentials; list/dict defaults |

### Advanced

| Concept | Description | Use in network automation |
|--------|-------------|----------------------------|
| `BaseSettings` | Load from environment variables (and .env) | App config, API keys, feature flags |
| Custom types | E.g. constrained types, custom validators | IP address, VLAN ID ranges |
| JSON schema | `model_json_schema()` for API docs or codegen | OpenAPI/FastAPI integration |
| FastAPI integration | Request/response models (brief) | Typed API bodies and responses |

## Use Cases in Network Automation

- **Device inventory**: Validate YAML/JSON inventory with a Pydantic model; fail fast on missing or invalid fields.
- **API responses**: Parse and validate NetBox, Nautobot, or custom API responses so the rest of the code uses typed objects.
- **Configuration**: Load app or tool config from env or files with `BaseSettings`; validate nested config (e.g. sources, cache TTL).
- **Reports**: Build validation reports (e.g. pre-flight checks) as nested Pydantic models for consistent structure and serialization.

## Related Modules and Projects

- **Module 12:** Advanced Patterns (decorators, FastAPI, SQLAlchemy)
- **automation-preflight:** `automation-preflight/models/device.py` — DeviceInventory, CheckResult, ValidationReport (in repo root)
- **news-sentiment-comparison:** `news_sentiment/config.py` — Nested config with BaseModel and Field (in repo root)

## Exercises

Work through `exercises.py` for fill-in-the-blank practice. There are **13 exercises**:

| # | Level       | Topic |
|---|-------------|--------|
| 1 | Beginner    | Device model, `model_validate`, `model_dump`, `validate_device_data` |
| 2 | Intermediate| `field_validator` (normalize hostname) |
| 3 | Intermediate| Nested model `list[Interface]`, `default_factory` |
| 4 | Advanced    | ValidationReport (nested CheckResult, summary fields) |
| 5 | Beginner    | JSON round-trip: `model_validate_json`, `model_dump_json` |
| 6 | Intermediate| Field constraints: `ge`, `le`, `gt` (port, timeout) |
| 7 | Intermediate| Inspect `ValidationError.errors()` for reporting |
| 8 | Intermediate| `model_validator` (cross-field: port or port_range) |
| 9 | Intermediate| `ConfigDict(extra="forbid")` |
| 10| Intermediate| Optional + `default_factory` for list/dict fields |
| 11| Advanced    | `BaseSettings` (env prefix; optional if pydantic-settings installed) |
| 12| Intermediate| Constrained type: VLAN ID `ge=1, le=4094` |
| 13| Beginner    | `model_json_schema()` and required fields |

## Examples

Review `examples.py` for runnable Device/Inventory models, validators, and an optional BaseSettings example.
