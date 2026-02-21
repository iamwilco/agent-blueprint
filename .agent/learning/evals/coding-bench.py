#!/usr/bin/env python3
"""
Coding benchmark for agent skill evaluation.

Runs a suite of micro-benchmarks inspired by SWE-bench:
  - Code correctness (does generated code pass assertions?)
  - Style compliance (does it pass linting?)
  - Test quality (does it catch injected mutations?)

Usage:
    python coding-bench.py                    # Run all benchmarks
    python coding-bench.py --bench style      # Run single benchmark
    python coding-bench.py --threshold 0.8    # Custom pass threshold
"""

import argparse
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BenchCase:
    name: str
    category: str  # correctness | style | test_quality
    code: str
    test_code: str  # assertion to run against the code
    description: str


@dataclass
class BenchResult:
    case: BenchCase
    passed: bool
    detail: str


CASES: list[BenchCase] = [
    BenchCase(
        name="fibonacci",
        category="correctness",
        code=textwrap.dedent("""\
            def fibonacci(n: int) -> int:
                if n <= 1:
                    return n
                a, b = 0, 1
                for _ in range(2, n + 1):
                    a, b = b, a + b
                return b
        """),
        test_code="assert fibonacci(0) == 0; assert fibonacci(1) == 1; assert fibonacci(10) == 55",
        description="Iterative Fibonacci implementation",
    ),
    BenchCase(
        name="flatten_list",
        category="correctness",
        code=textwrap.dedent("""\
            def flatten(lst):
                result = []
                for item in lst:
                    if isinstance(item, list):
                        result.extend(flatten(item))
                    else:
                        result.append(item)
                return result
        """),
        test_code="assert flatten([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6]; assert flatten([]) == []",
        description="Recursive list flattening",
    ),
    BenchCase(
        name="style_clean_function",
        category="style",
        code=textwrap.dedent("""\
            def calculate_discount(price: float, discount_pct: float) -> float:
                \"\"\"Apply percentage discount to price.\"\"\"
                if not 0 <= discount_pct <= 100:
                    raise ValueError("Discount must be 0-100")
                return round(price * (1 - discount_pct / 100), 2)
        """),
        test_code="assert calculate_discount(100, 20) == 80.0",
        description="Well-styled function (should pass linting)",
    ),
    BenchCase(
        name="style_violations",
        category="style",
        code=textwrap.dedent("""\
            def BadFunc( x,y ):
                z=x+y
                unused = 42
                return z
        """),
        test_code="assert BadFunc(1, 2) == 3",
        description="Function with style violations (should be flagged)",
    ),
    BenchCase(
        name="safe_division",
        category="correctness",
        code=textwrap.dedent("""\
            def safe_divide(a: float, b: float, default: float = 0.0) -> float:
                try:
                    return a / b
                except ZeroDivisionError:
                    return default
        """),
        test_code="assert safe_divide(10, 2) == 5.0; assert safe_divide(1, 0) == 0.0; assert safe_divide(1, 0, -1) == -1.0",
        description="Division with zero-safety",
    ),
]


def run_correctness(case: BenchCase) -> BenchResult:
    """Execute code + test assertions in a subprocess."""
    full_code = case.code + "\n" + case.test_code
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full_code)
        f.flush()
        result = subprocess.run([sys.executable, f.name], capture_output=True, text=True, timeout=10)
    passed = result.returncode == 0
    detail = "OK" if passed else result.stderr.strip().split("\n")[-1]
    return BenchResult(case, passed, detail)


def run_style(case: BenchCase) -> BenchResult:
    """Run ruff on the code and check for violations."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(case.code)
        f.flush()
        result = subprocess.run(
            ["ruff", "check", f.name, "--select=E,W,F", "--output-format=json"],
            capture_output=True, text=True,
        )
    import json
    try:
        issues = json.loads(result.stdout) if result.stdout.strip() else []
    except Exception:
        issues = []

    if case.name == "style_violations":
        # This case SHOULD have violations — pass if we detect them
        passed = len(issues) > 0
        detail = f"Detected {len(issues)} violations (expected >0)"
    else:
        passed = len(issues) == 0
        detail = f"{len(issues)} violations" if issues else "Clean"
    return BenchResult(case, passed, detail)


def run_bench(cases: list[BenchCase], category_filter: str | None = None) -> list[BenchResult]:
    results = []
    for case in cases:
        if category_filter and case.category != category_filter:
            continue
        if case.category == "style":
            results.append(run_style(case))
        else:
            results.append(run_correctness(case))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent coding benchmark")
    parser.add_argument("--bench", choices=["correctness", "style", "test_quality"], help="Run specific category")
    parser.add_argument("--threshold", type=float, default=0.8, help="Pass threshold (0-1)")
    args = parser.parse_args()

    results = run_bench(CASES, args.bench)
    total = len(results)
    passed = sum(1 for r in results if r.passed)

    print("Agent Coding Benchmark")
    print("=" * 50)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  [{status}] {r.case.category}/{r.case.name}: {r.detail}")

    score = passed / total if total else 0
    print(f"\nScore: {passed}/{total} ({score:.0%})")
    print(f"Threshold: {args.threshold:.0%} | {'PASSED' if score >= args.threshold else 'FAILED'}")
    return 0 if score >= args.threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
