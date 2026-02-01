"""
Terraform CLI driver: run Terraform from Python, parse plan summary.

Goal:
  - Run terraform init/validate/plan from Python in a given directory.
  - Parse the plan summary line ("Plan: X to add, Y to change, Z to destroy")
    into a dict so Python can use it (e.g. CI gates, reporting).
"""

import re
import subprocess
from pathlib import Path


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences (e.g. \\x1b[1m) so regex can match 'Plan: N to add...'."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def run_terraform(working_dir: Path, *args: str) -> subprocess.CompletedProcess:
    """
    Run terraform with given args; cwd=working_dir, capture stdout/stderr. Return CompletedProcess.

    working_dir: directory containing .tf files (Terraform runs with this as cwd).
    *args: terraform subcommand and options, e.g. "init", "validate", ("plan", "-input=false").

    CompletedProcess is a class that represents the result of a subprocess.run() call.
    It has three attributes:
    - returncode: the exit status of the subprocess
    - stdout: the standard output of the subprocess
    - stderr: the standard error of the subprocess

    The run() function returns a CompletedProcess object.
    The run() function takes the following arguments:
    - args: a list of arguments to pass to the subprocess
    """
    return subprocess.run( # the subprocess is a function that runs a command and returns a CompletedProcess object.
        ["terraform", *args], #is terraform the command? yes, terraform is the command.
        cwd=working_dir,  # Terraform runs in this directory (must contain .tf files).
        capture_output=True, # capture the standard output and standard error of the subprocess
        text=True, # return the output as a string
    )


def parse_plan_summary(stdout: str) -> dict[str, int] | None:
    """
    Extract 'Plan: X to add, Y to change, Z to destroy' from terraform plan output.

    stdout: full text of `terraform plan` output (may be from stdout or stderr; Terraform often uses stderr).
    Returns: {"add": N, "change": N, "destroy": N}, or None if the summary line wasn't found.
    """
    # Terraform 1.x prints "Plan: N to add, N to change, N to destroy." when there are changes.
    match = re.search( # where is re defined? it is defined in the re module.
        r"Plan:\s+(\d+)\s+to\s+add,\s+(\d+)\s+to\s+change,\s+(\d+)\s+to\s+destroy\.?",
        stdout, #we are not searching through re, we are searching through stdout using the re search function from the re module.
    )
    if match:
        return {
            "add": int(match.group(1)), # match has group methods that return the groups of the match. how many groups are there? there are 3 groups. so group 1 is always add? yes, group 1 is always add.
            "change": int(match.group(2)), # how do we know which group to use? we use the group number that is passed to the group method.
            "destroy": int(match.group(3)),
        }
    # When nothing to do, Terraform prints "No changes. Your infrastructure matches the configuration."
    if re.search(r"No changes", stdout, re.IGNORECASE):
        return {"add": 0, "change": 0, "destroy": 0}
    return None


def main() -> None:  #this none is optional, but it is a good practice to specify the return type of the function.
    # Run init -> validate -> plan in minimal/ (no cloud provider needed).
    base = Path(__file__).parent
    minimal_dir = base / "minimal"

    init_result = run_terraform(minimal_dir, "init") #what does 'init' do? it initializes the terraform state file.
    #what does the state file look like before 'init'? it is empty. then it contains the state of the terraform resources.


    if init_result.returncode == 0:
        print("terraform init: OK")
    else:
        print("terraform init: FAILED")
        print(init_result.stderr or init_result.stdout) #this will print the first one that is not none? yes, it will print the first one that is not none.

    validate_result = run_terraform(minimal_dir, "validate") #what does 'validate' do? it validates the terraform configuration for syntax, structure and provider requireents during init.
    if validate_result.returncode == 0:
        print("terraform validate: OK")
    else:
        print("terraform validate: FAILED")
        print(validate_result.stderr or validate_result.stdout)

    # -input=false avoids interactive prompts when running non-interactively.
    plan_result = run_terraform(minimal_dir, "plan", "-input=false")  #i can pass any number of arguments to the run_terraform function.
    
    if plan_result.returncode == 0:
        print("terraform plan: OK")
        # Terraform often sends plan text to stderr; try stdout first, then stderr.
        plan_text = plan_result.stdout or plan_result.stderr or ""
        
        # Strip ANSI codes so regex can match (e.g. \x1b[1mPlan:\x1b[0m -> Plan:).
        plan_text_plain = _strip_ansi(plan_text)
        summary = parse_plan_summary(plan_text_plain)
        if summary is not None:
            print("Plan summary:", summary)
        else:
            print("Plan summary: (could not parse)")
    else:
        print("terraform plan: FAILED")
        print(plan_result.stderr or plan_result.stdout)


if __name__ == "__main__":
    main()
