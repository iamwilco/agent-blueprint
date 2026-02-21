#!/usr/bin/env python3
"""Evaluator for code-review skill: inject known bugs, measure detection rate."""

import subprocess
import json
import tempfile
import textwrap
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BugCase:
    name: str
    code: str
    expected_issues: int
    description: str


@dataclass
class EvalResult:
    case_name: str
    expected: int
    found: int
    passed: bool


CASES: list[BugCase] = [
    BugCase(
        name="sql-injection",
        code=textwrap.dedent("""\
            def get_user(db, user_id):
                query = f"SELECT * FROM users WHERE id = {user_id}"
                return db.execute(query)
        """),
        expected_issues=1,
        description="Unparameterized SQL query",
    ),
    BugCase(
        name="missing-return",
        code=textwrap.dedent("""\
            def divide(a: int, b: int) -> float:
                if b != 0:
                    return a / b
        """),
        expected_issues=1,
        description="Missing return on else branch",
    ),
    BugCase(
        name="unused-variable",
        code=textwrap.dedent("""\
            def process(items):
                result = []
                temp = "unused"
                for item in items:
                    result.append(item.strip())
                return result
        """),
        expected_issues=1,
        description="Unused variable 'temp'",
    ),
    BugCase(
        name="broad-except",
        code=textwrap.dedent("""\
            def fetch_data(url):
                try:
                    import urllib.request
                    return urllib.request.urlopen(url).read()
                except:
                    pass
        """),
        expected_issues=1,
        description="Bare except swallows all errors",
    ),
    BugCase(
        name="mutable-default",
        code=textwrap.dedent("""\
            def append_item(item, target=[]):
                target.append(item)
                return target
        """),
        expected_issues=1,
        description="Mutable default argument",
    ),
]


def run_ruff_check(code: str) -> int:
    """Write code to temp file, run ruff, return issue count."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        result = subprocess.run(
            ["ruff", "check", f.name, "--output-format=json", "--select=ALL"],
            capture_output=True, text=True,
        )
    try:
        issues = json.loads(result.stdout) if result.stdout.strip() else []
        return len(issues)
    except json.JSONDecodeError:
        return 0


def evaluate() -> list[EvalResult]:
    results = []
    for case in CASES:
        found = run_ruff_check(case.code)
        passed = found >= case.expected_issues
        results.append(EvalResult(case.name, case.expected_issues, found, passed))
    return results


def main() -> int:
    results = evaluate()
    total = len(results)
    passed = sum(1 for r in results if r.passed)

    print("Code Review Skill Eval")
    print("=" * 40)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] {r.case_name}: expected>={r.expected}, found={r.found}")
    print(f"\nScore: {passed}/{total} ({passed/total:.0%})")
    print(f"Threshold: 80% | {'PASSED' if passed/total >= 0.8 else 'FAILED'}")
    return 0 if passed / total >= 0.8 else 1


if __name__ == "__main__":
    raise SystemExit(main())
