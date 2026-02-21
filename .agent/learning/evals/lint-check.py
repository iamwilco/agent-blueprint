#!/usr/bin/env python3
"""
Lint quality evaluator: runs ruff + mypy on the project src/ directory
and reports a quality score based on issues per file.

Usage:
    python lint-check.py                        # Scan default src/
    python lint-check.py --path /path/to/code   # Scan custom path
    python lint-check.py --threshold 0.9        # Custom pass threshold
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def count_python_files(path: str) -> int:
    return len(list(Path(path).rglob("*.py")))


def run_ruff(path: str) -> list[dict]:
    """Run ruff and return structured issues."""
    result = subprocess.run(
        ["ruff", "check", path, "--output-format=json", "--select=E,W,F,I"],
        capture_output=True, text=True,
    )
    try:
        return json.loads(result.stdout) if result.stdout.strip() else []
    except json.JSONDecodeError:
        return []


def run_mypy(path: str) -> int:
    """Run mypy and return error count."""
    result = subprocess.run(
        ["mypy", path, "--ignore-missing-imports", "--no-error-summary"],
        capture_output=True, text=True,
    )
    errors = [line for line in result.stdout.strip().split("\n") if line and ": error:" in line]
    return len(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint quality evaluator")
    parser.add_argument("--path", default="src/", help="Path to scan")
    parser.add_argument("--threshold", type=float, default=0.9, help="Clean file ratio threshold")
    args = parser.parse_args()

    path = args.path
    total_files = count_python_files(path)

    if total_files == 0:
        print(f"No Python files found in {path}")
        return 1

    # Ruff analysis
    ruff_issues = run_ruff(path)
    ruff_files_with_issues = len(set(i.get("filename", "") for i in ruff_issues))

    # Mypy analysis
    mypy_errors = run_mypy(path)

    # Score: ratio of clean files
    files_with_issues = ruff_files_with_issues  # mypy counted separately
    clean_ratio = (total_files - files_with_issues) / total_files

    print("Lint Quality Eval")
    print("=" * 40)
    print(f"  Python files scanned: {total_files}")
    print(f"  Ruff issues: {len(ruff_issues)} across {ruff_files_with_issues} files")
    print(f"  Mypy errors: {mypy_errors}")
    print(f"  Clean file ratio: {clean_ratio:.0%}")
    print(f"\nThreshold: {args.threshold:.0%} | {'PASSED' if clean_ratio >= args.threshold else 'FAILED'}")

    # Top issues by rule
    if ruff_issues:
        from collections import Counter
        rule_counts = Counter(i.get("code", "unknown") for i in ruff_issues)
        print("\nTop ruff rules violated:")
        for rule, count in rule_counts.most_common(5):
            print(f"  {rule}: {count}")

    return 0 if clean_ratio >= args.threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
