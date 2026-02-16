#!/usr/bin/env python3
"""
Run terraform init and plan from Python; print return code and plan summary.
Demo for terraform-lessons 04_python_integration. Run from 04_python_integration directory:
  python examples/run_terraform.py
"""
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


def run_terraform(working_dir: Path, *args: str) -> subprocess.CompletedProcess:
    """Run terraform with given args; cwd=working_dir; capture stdout/stderr. Return CompletedProcess."""
    return subprocess.run(
        ["terraform", *args],
        cwd=working_dir,
        capture_output=True,
        text=True,
    )


def parse_plan_summary(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract plan summary from terraform plan output.
    Returns dict with add, change, destroy keys, or None if 'No changes' or not found.
    """
    if not text:
        return None
    if "No changes" in text or "no changes" in text.lower():
        return {"add": 0, "change": 0, "destroy": 0}
    # e.g. "Plan: 1 to add, 0 to change, 1 to destroy."
    match = re.search(
        r"Plan:\s*(\d+)\s*to\s*add,\s*(\d+)\s*to\s*change,\s*(\d+)\s*to\s*destroy",
        text,
    )
    if match:
        return {
            "add": int(match.group(1)),
            "change": int(match.group(2)),
            "destroy": int(match.group(3)),
        }
    return None


def main() -> None:
    base = Path(__file__).resolve().parent
    minimal_dir = base / "minimal"
    if not minimal_dir.exists():
        print("minimal/ not found at", minimal_dir)
        return

    print("Running terraform init...")
    init_result = run_terraform(minimal_dir, "init")
    print("  Return code:", init_result.returncode)
    if init_result.returncode != 0:
        print("  stderr:", (init_result.stderr or "")[:300])
        return

    print("Running terraform plan -input=false...")
    plan_result = run_terraform(minimal_dir, "plan", "-input=false")
    print("  Return code:", plan_result.returncode)
    output = (plan_result.stdout or "") + (plan_result.stderr or "")
    summary = parse_plan_summary(output)
    if summary is not None:
        print("  Plan summary:", summary)
    else:
        print("  (Summary not parsed; check output)")


if __name__ == "__main__":
    main()
