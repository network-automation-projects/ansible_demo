# Ready-to-use pathlib snippets.
# Prefer Path over os.path and string concatenation. See python-from-basic-to-tools.md

from pathlib import Path

# -----------------------------------------------------------------------------
# Path construction — cross-platform, composable
# -----------------------------------------------------------------------------

# base = Path(".")
# config_file = base / "config" / "settings.yaml"
# output_dir = Path.home() / "output" / "reports"

# -----------------------------------------------------------------------------
# Read / write text files
# -----------------------------------------------------------------------------

# content = path.read_text()
# path.write_text("hello\n")

# With encoding:
# content = path.read_text(encoding="utf-8")
# path.write_text("hello\n", encoding="utf-8")

# -----------------------------------------------------------------------------
# Existence and type checks
# -----------------------------------------------------------------------------

# if path.exists():
#     ...
# if path.is_file():
#     ...
# if path.is_dir():
#     ...

# -----------------------------------------------------------------------------
# Common operations
# -----------------------------------------------------------------------------

# path.mkdir(parents=True, exist_ok=True)  # create dirs
# path.unlink()  # delete file
# path.rename(new_path)  # move/rename
# list(path.iterdir())  # list contents
# path.glob("*.py")  # match pattern
# path.resolve()  # absolute path
