// solution-go.go — Terraform CLI driver in Go.
// Run terraform init/validate/plan, parse plan summary.
// Run from terraform_python_driver/ so minimal/ is found (e.g. go run solution-go.go).

package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

// stripANSI removes ANSI escape sequences so regex can match "Plan: N to add...".
func stripANSI(text string) string {
	ansi := regexp.MustCompile(`\x1b\[[0-9;]*m`)
	return ansi.ReplaceAllString(text, "")
}

// RunTerraform runs terraform with given args in workingDir; returns combined output and exit code.
func RunTerraform(workingDir string, args ...string) (output string, exitCode int, err error) {
	cmd := exec.Command("terraform", args...)
	cmd.Dir = workingDir
	out, err := cmd.CombinedOutput()
	output = string(out)
	if cmd.ProcessState != nil {
		exitCode = cmd.ProcessState.ExitCode()
	}
	return output, exitCode, err
}

// PlanSummary holds add/change/destroy counts from "Plan: X to add, Y to change, Z to destroy".
type PlanSummary struct {
	Add     int
	Change  int
	Destroy int
}

// ParsePlanSummary extracts the plan summary line from terraform plan output.
// Returns nil if the summary line wasn't found.
func ParsePlanSummary(stdout string) *PlanSummary {
	plain := stripANSI(stdout)
	re := regexp.MustCompile(`Plan:\s+(\d+)\s+to\s+add,\s+(\d+)\s+to\s+change,\s+(\d+)\s+to\s+destroy\.?`)
	matches := re.FindStringSubmatch(plain)
	if len(matches) == 4 {
		add, _ := strconv.Atoi(matches[1])
		chg, _ := strconv.Atoi(matches[2])
		destroy, _ := strconv.Atoi(matches[3])
		return &PlanSummary{Add: add, Change: chg, Destroy: destroy}
	}
	if strings.Contains(strings.ToLower(plain), "no changes") {
		return &PlanSummary{Add: 0, Change: 0, Destroy: 0}
	}
	return nil
}

func main() {
	cwd, err := os.Getwd()
	if err != nil {
		fmt.Fprintln(os.Stderr, "getwd:", err)
		os.Exit(1)
	}
	minimalDir := filepath.Join(cwd, "minimal")

	// init
	out, code, _ := RunTerraform(minimalDir, "init")
	if code == 0 {
		fmt.Println("terraform init: OK")
	} else {
		fmt.Println("terraform init: FAILED")
		fmt.Print(out)
	}

	// validate
	out, code, _ = RunTerraform(minimalDir, "validate")
	if code == 0 {
		fmt.Println("terraform validate: OK")
	} else {
		fmt.Println("terraform validate: FAILED")
		fmt.Print(out)
	}

	// plan
	out, code, _ = RunTerraform(minimalDir, "plan", "-input=false")
	if code == 0 {
		fmt.Println("terraform plan: OK")
		summary := ParsePlanSummary(out)
		if summary != nil {
			fmt.Printf("Plan summary: add=%d change=%d destroy=%d\n", summary.Add, summary.Change, summary.Destroy)
		} else {
			fmt.Println("Plan summary: (could not parse)")
		}
	} else {
		fmt.Println("terraform plan: FAILED")
		fmt.Print(out)
	}
}
