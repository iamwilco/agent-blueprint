# Skill: Code Reviewer
**Domain:** coding
**Version:** 1.0
**Eval Score:** —

## Description
Perform structured code review: identify bugs, security issues, test gaps, style violations, and performance concerns. Output actionable findings with severity and suggested fixes.

## Usage
1. Read the diff or file(s) under review.
2. Run through the checklist below for each changed function/block.
3. Output findings in structured format (severity, location, description, suggestion).
4. Summarize: total findings by severity, overall quality score (0-10).

## Checklist
- **Correctness:** Logic errors, off-by-one, null/undefined handling.
- **Security:** Injection, auth bypass, secret exposure, unsafe deserialization.
- **Error handling:** Missing try/catch, swallowed exceptions, unclear error messages.
- **Test coverage:** New code paths without tests, weakened existing tests.
- **Performance:** N+1 queries, unnecessary allocations, blocking I/O in async context.
- **Style:** Naming conventions, dead code, excessive complexity (cyclomatic >10).
- **Backward compatibility:** Breaking API changes without versioning.

## Code Snippet
```python
import subprocess, json

def review_code(file_path: str) -> list[dict]:
    findings = []
    # Static analysis pass
    result = subprocess.run(["ruff", "check", file_path, "--output-format=json"], capture_output=True, text=True)
    if result.stdout:
        for issue in json.loads(result.stdout):
            findings.append({"severity": "warning", "location": f"{file_path}:{issue['location']['row']}", "description": issue["message"], "suggestion": f"Fix {issue['code']}"})
    # Type check pass
    mypy = subprocess.run(["mypy", file_path, "--no-error-summary"], capture_output=True, text=True)
    for line in mypy.stdout.strip().split("\n"):
        if line:
            findings.append({"severity": "error", "location": file_path, "description": line, "suggestion": "Fix type error"})
    return findings
```

## Eval Method
- **Metric:** Finding recall — inject 5 known bugs into a sample file; measure how many the reviewer catches.
- **Script:** `eval.py` in this directory.
- **Threshold:** ≥4/5 findings detected = pass.