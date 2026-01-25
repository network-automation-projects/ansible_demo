# AGENTS.md — ConceptProjects

## Build / Run / Test
- Python version: 3.9+
- Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt` (if present)
- Run script: `python <script>.py`
- Lint (syntax): `python -m py_compile <script>.py`
- Format (recommended): `black .`
- Run all tests: `pytest`
- Run single test: `pytest path/to/test_file.py::test_name`

## Code Style Guidelines
- Formatting: Black defaults (88 chars); no manual alignment
- Imports: stdlib → third‑party → local, one per line
- Types: add type hints to public functions where practical
- Naming: `snake_case` functions/vars, `UPPER_CASE` constants, clear names
- Errors: catch specific exceptions; fail fast with clear messages
- Logging: use `logging`; avoid `print` in non‑CLI code
- Paths/I/O: use `pathlib`; no hardcoded absolute paths
- Secrets: never commit credentials; use env vars or config files

## Notes
- Prefer small, composable scripts over large frameworks
- No Cursor or Copilot rules detected at repo root