"""
Exercise: convert dict to tfvars, write tfvars file, validate required keys in tfvars.
Fill in the TODOs. See README.md for the problem description.
"""

from pathlib import Path


def dict_to_tfvars(variables: dict[str, str | int | bool]) -> str:
    """Convert flat dict to HCL tfvars content. Strings quoted, numbers/bools unquoted. Keys sorted."""
    # TODO: lines = []; for k in sorted(variables): v = variables[k]
    # TODO: if isinstance(v, str): line = f'{k} = "{v}"'; elif isinstance(v, bool): line = f'{k} = {str(v).lower()}'
    # TODO: else: line = f'{k} = {v}'; lines.append(line)
    # TODO: return "\n".join(lines)
    return ""


def write_tfvars(path: Path, variables: dict[str, str | int | bool]) -> None:
    """Write dict_to_tfvars(variables) to path. Use UTF-8."""
    # TODO: path.write_text(dict_to_tfvars(variables), encoding="utf-8")
    pass


def validate_tfvars_keys(path: Path, required: set[str]) -> tuple[bool, set[str]]:
    """
    Read tfvars at path (key=value lines; first = splits; strip; skip blank and #).
    Return (all_required_present, missing_keys).
    """
    # TODO: keys = set(); open path, for each line: strip, skip blank and startswith('#')
    # TODO: if '=' in line: key, _, _ = line.partition('='); keys.add(key.strip())
    # TODO: missing = required - keys; return (len(missing) == 0, missing)
    return (False, set())


def main() -> None:
    base = Path(__file__).parent
    # TODO: variables = {"aws_region": "us-east-1", "instance_type": "t2.micro", "enable_nat_gateway": True}
    # TODO: write_tfvars(base / "terraform.tfvars", variables)
    # TODO: required = {"aws_region", "instance_type"}
    # TODO: ok, missing = validate_tfvars_keys(base / "terraform.tfvars", required)
    # TODO: print("All required present:", ok); print("Missing:", missing)
    pass


if __name__ == "__main__":
    main()
