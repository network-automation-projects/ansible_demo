# real-python-tools

Ready-to-use code snippets from Real Python and workplace patterns. Copy-paste into your project as needed.

For the "learn this → replace with" reference chart, see [python-from-basic-to-tools.md](../python-from-basic-to-tools.md).

---

## Index

| File | Snippets | When to use |
|------|----------|-------------|
| [decorators.py](decorators.py) | `timer`, `debug`, `register`, `task`, `slow_down` | Timing, logging, plugin/task registries |
| [timing.py](timing.py) | `perf_counter`, `timeit`, `monotonic` | Single-run timing, benchmarking, clock-skew-safe duration |
| [paths.py](paths.py) | `Path` construction, read/write, exists | Cross-platform file paths and I/O |
| [config.py](config.py) | `os.environ`, `pydantic-settings` | Env vars, typed config with validation |
| [retries.py](retries.py) | `@retry` with tenacity | Exponential backoff, resilient API calls |
