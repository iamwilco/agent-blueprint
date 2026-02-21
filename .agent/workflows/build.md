# Build Workflow
**Trigger:** `/build`

## Graph
```
[START] → pull_latest → install_deps → lint_check
  → {lint_pass?} → build → {build_pass?} → report_success → [END]
                                         → diagnose_failure → report_failure → [END]
              → fix_lint → lint_check (retry max 2)
```

## Nodes

### 1. pull_latest
```bash
git checkout main && git pull origin main
```
**Exit:** proceed to `install_deps`.

### 2. install_deps
```bash
pip install -r requirements.txt   # Python
# npm ci                          # Node.js
```
**Exit:** proceed to `lint_check`.

### 3. lint_check
```bash
ruff check src/ --fix && mypy src/
```
**Exit:** if exit code 0 → `build`; else → `fix_lint` (max 2 retries, then fail).

### 4. fix_lint
Agent auto-fixes lint issues using `ruff check --fix`. Commit with `chore(lint): auto-fix`.
**Exit:** retry `lint_check`.

### 5. build
```bash
docker compose build
# or: python -m build / npm run build
```
**Exit:** if exit code 0 → `report_success`; else → `diagnose_failure`.

### 6. diagnose_failure
Parse build logs. Identify: missing imports, syntax errors, type mismatches. Output top 3 likely root causes.

### 7. report_success / report_failure
Log result to `learning/reflection-log.md`. Update `learning/memory.json` with build outcome.
