"""
Generate terraform.tfvars from a dict and validate required keys in a tfvars file.
"""

from pathlib import Path


def dict_to_tfvars(variables: dict[str, str | int | bool]) -> str:
    """Convert flat dict to HCL tfvars content. Strings quoted, numbers/bools unquoted. Keys sorted."""
    lines: list[str] = []
    for k in sorted(variables):
        v = variables[k]
        if isinstance(v, str):
            # Escape internal double quotes for HCL (so HCL needs the escaped string, python doesn't care either way)
            escaped = v.replace("\\", "\\\\").replace('"', '\\"')
            line = f'{k} = "{escaped}"'
        elif isinstance(v, bool):
            line = f"{k} = {str(v).lower()}"
        else:
            line = f"{k} = {v}"
        lines.append(line)
    return "\n".join(lines)


def write_tfvars(path: Path, variables: dict[str, str | int | bool]) -> None:
    """Write dict_to_tfvars(variables) to path. Use UTF-8."""
    path.write_text(dict_to_tfvars(variables), encoding="utf-8")


def validate_tfvars_keys(path: Path, required: set[str]) -> tuple[bool, set[str]]:
    #the incoming set is the set of required keys.
    """
    Read tfvars at path (key=value lines; first = splits; strip; skip blank and #).
    Return (all_required_present, missing_keys).  #does this mean that if all the required keys are present, then the function returns True, and if not, then the function returns False? yes, it means that if all the required keys are present, then the function returns True, and if not, then the function returns False.
    """
    keys: set[str] = set()                    #? why do we set a set equal to a set? because a set is a collection of unique elements. so we can add the keys to the set and then check if the set is equal to the required set.       
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, _ = line.partition("=")  #is this the split? yes, it is the split.
                keys.add(key.strip())
    missing = required - keys
    return (len(missing) == 0, missing) #so missing can be the empty set, and then the function returns True, and if not, then the function returns False.


def main() -> None:
    base = Path(__file__).parent                # is this standard practice? yes, it is standard practice to use the parent directory of the current file. because the current file is the exercise.py file, and the parent directory is the directory that contains the exercise.py file.
    variables: dict[str, str | int | bool] = {
        "aws_region": "us-east-1",
        "instance_type": "t2.micro",
        "enable_nat_gateway": True,
    }
    tfvars_path = base / "terraform.tfvars"
    write_tfvars(tfvars_path, variables)
    print("Wrote", tfvars_path)

    required = {"aws_region", "instance_type"}
    ok, missing = validate_tfvars_keys(tfvars_path, required)
    print("All required present:", ok)
    print("Missing:", missing)


if __name__ == "__main__":
    main()
