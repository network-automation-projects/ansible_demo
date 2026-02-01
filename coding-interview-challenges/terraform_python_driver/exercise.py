"""
Exercise: run Terraform from Python, parse plan summary.
Fill in the TODOs. See README.md for the problem description.
"""

import re
import subprocess
from pathlib import Path

def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences (e.g. \\x1b[1m) so regex can match 'Plan: N to add...'."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def run_terraform(working_dir: Path, *args: str) -> subprocess.CompletedProcess:
    """Run terraform with given args; cwd=working_dir, capture stdout/stderr. Return CompletedProcess."""
                                                                # TODO: subprocess.run(["terraform", *args], cwd=working_dir, capture_output=True, text=True)
    result = subprocess.run(
        ["terraform", *args],
        cwd = working_dir,
        capture_output=True,   # are there other optional inputs for the subprocess.run function? yes, there are other optional inputs for the subprocess.run function. check the documentation for the subprocess.run function.
        text=True
    )
    return result
    
    #raise NotImplementedError("TODO: implement run_terraform")


def parse_plan_summary(stdout: str) -> dict[str, int] | None:
    """Extract 'Plan: X to add, Y to change, Z to destroy' from stdout. Return dict or None."""
                                                                # TODO: regex for "Plan: N to add, N to change, N to destroy" (or "no changes")
                                                                # TODO: return {"add": int, "change": int, "destroy": int} or None
    #search the incoming stdout string for the three groups
    groups = re.search(
        r"Plan:\s+(\d+)\s+to\s+add,\s+(\d+)\s+to\s+change,\s+(\d+)\s+to\s+destroy\.?",
        stdout,        #we are not searching through re, we are searching through stdout using the re search function from the re module.
    )

    if groups:
        return{"add": int(groups.group(1)),
                "change": int(groups.group(2)),
                "destroy": int(groups.group(3)),
        }

    if re.search(r"No changes", stdout, re.IGNORECASE):
        return {"add": 0, "change": 0, "destroy": 0}
    return None


def main() -> None:
    base = Path(__file__).parent
    minimal_dir = base / "minimal"

    # TODO: run terraform init, print success/failure (returncode == 0)
    init_result = run_terraform(minimal_dir, "init")

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




#CLEAN COPY
# """
# Exercise: run Terraform from Python, parse plan summary.
# Fill in the TODOs. See README.md for the problem description.
# """

# import re
# import subprocess
# from pathlib import Path


# def run_terraform(working_dir: Path, *args: str) -> subprocess.CompletedProcess:
#     """Run terraform with given args; cwd=working_dir, capture stdout/stderr. Return CompletedProcess."""
#                                                                 # TODO: subprocess.run(["terraform", *args], cwd=working_dir, capture_output=True, text=True)
#     raise NotImplementedError("TODO: implement run_terraform")


# def parse_plan_summary(stdout: str) -> dict[str, int] | None:
#     """Extract 'Plan: X to add, Y to change, Z to destroy' from stdout. Return dict or None."""
#                                                                 # TODO: regex for "Plan: N to add, N to change, N to destroy" (or "no changes")
#                                                                 # TODO: return {"add": int, "change": int, "destroy": int} or None
#     return None


# def main() -> None:
#     base = Path(__file__).parent
#     minimal_dir = base / "minimal"

#                                                                 # TODO: run terraform init, print success/failure (returncode == 0)
#                                                                 # TODO: run terraform validate, print success/failure
#                                                                 # TODO: run terraform plan -input=false, print success/failure and parse_plan_summary(stdout)
#     pass


# if __name__ == "__main__":
#     main()
