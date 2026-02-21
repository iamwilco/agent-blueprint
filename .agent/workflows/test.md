# Test Workflow
**Trigger:** `/test`

## Graph
```
[START] → detect_changes → select_suites → run_fast_tests
  → {fast_pass?} → run_full_suite → {full_pass?} → report_success → [END]
                                                  → diagnose_failures → suggest_fix → [END]
               → diagnose_failures → suggest_fix → [END]
```

## Nodes

### 1. detect_changes
```bash
git diff --name-only HEAD~1..HEAD
```
Identify changed modules to scope test selection.

### 2. select_suites
Map changed files to test directories:
| Changed Path | Test Suite |
|---|---|
| `src/api/` | `tests/unit/test_api.py` + `tests/integration/` |
| `src/worker/` | `tests/unit/test_worker.py` |
| `frontend/` | `npm test -- --changedSince=HEAD~1` |

### 3. run_fast_tests
```bash
pytest tests/unit/ -x --timeout=30 -q
```
**Exit:** if pass → `run_full_suite`; if fail → `diagnose_failures`.

### 4. run_full_suite
```bash
pytest tests/ --cov=src --cov-report=term-missing --timeout=120
```
**Exit:** if pass → `report_success`; if fail → `diagnose_failures`.

### 5. diagnose_failures
For each failure:
- Parse traceback → identify root cause file + line.
- Check git blame → was this line recently changed?
- Classify: regression, new bug, flaky test, environment issue.

### 6. suggest_fix
Output per failure:
- **Root cause:** one-sentence explanation.
- **Suggested fix:** minimal code change (diff format).
- **Regression test:** new test case to prevent recurrence.

### 7. report_success
```
Coverage: XX% (target: 80%)
All N tests passed in Xs.
```
Log to `learning/reflection-log.md`.
