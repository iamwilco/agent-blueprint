# Workflow: Dependency Update
**Trigger:** `/deps-update` or weekly schedule
**Goal:** Audit, update, and validate project dependencies safely.

## Graph
```
[START] → Inventory → Audit → Categorize → {has_critical?}
  → YES → Update_Critical → Test → {tests_pass?}
    → YES → Commit_Critical → Update_Minor → Test → Commit_Minor → [END]
    → NO  → Rollback → Report_Failure → [END]
  → NO  → Update_Minor → Test → {tests_pass?}
    → YES → Commit_Minor → [END]
    → NO  → Rollback → Report_Failure → [END]
```

## State
```python
class DepsState(TypedDict):
    inventory: list[dict]       # All current dependencies with versions
    outdated: list[dict]        # Dependencies with available updates
    critical: list[dict]        # Security vulnerabilities or major bumps
    minor: list[dict]           # Patch/minor updates
    test_results: dict          # Test suite results after update
    commits: list[str]          # Commit hashes for updates
    rollback_needed: bool
```

## Nodes

### 1. Inventory
Catalog all current dependencies and their versions.
```bash
# Python
pip list --format=json > deps-inventory.json
pip list --outdated --format=json > deps-outdated.json

# Node.js
npm ls --json > deps-inventory.json
npm outdated --json > deps-outdated.json

# General
cat requirements.txt  # or package.json, go.mod, Cargo.toml, etc.
```

### 2. Audit
Check for known security vulnerabilities.
```bash
# Python
pip-audit --format=json --output=audit-results.json

# Node.js
npm audit --json > audit-results.json

# General
# Check CVE databases, GitHub security advisories
```

### 3. Categorize
Split outdated packages into two groups:
- **Critical:** Security vulnerabilities, deprecated packages, packages 2+ major versions behind.
- **Minor:** Patch updates, minor version bumps with no known issues.

```python
def categorize(outdated: list, audit: list) -> tuple[list, list]:
    vuln_packages = {item["name"] for item in audit if item.get("vulnerability")}
    critical = [p for p in outdated if p["name"] in vuln_packages or is_major_bump(p)]
    minor = [p for p in outdated if p not in critical]
    return critical, minor
```

### 4. Update_Critical
Update critical packages one at a time to isolate breakage.
```bash
# Python — one at a time
pip install --upgrade <package>==<target_version>

# Node.js
npm install <package>@<target_version>
```

After each critical update:
- Run the full test suite.
- If tests fail, revert that single package and report it.

### 5. Update_Minor
Batch-update all minor/patch versions.
```bash
# Python
pip install --upgrade <pkg1> <pkg2> <pkg3>

# Node.js
npm update
```

### 6. Test
Run the full test suite after updates.
```bash
pytest tests/ --tb=short -q
# or: npm test
```

**Pass criteria:** All tests pass. No new warnings related to updated packages.

### 7. Commit
Commit updates with a clear message listing what changed.
```bash
# Critical updates — one commit per package
git add requirements.txt  # or package-lock.json
git commit -m "fix(deps): update <package> to <version> (security: CVE-XXXX-XXXXX)"

# Minor updates — batch commit
git add requirements.txt
git commit -m "chore(deps): batch update minor/patch dependencies

Updated:
- pkg-a 1.2.3 → 1.2.5
- pkg-b 3.0.1 → 3.1.0
- pkg-c 0.9.8 → 0.9.9"
```

### 8. Rollback
If tests fail after updates:
```bash
git checkout -- requirements.txt  # or package-lock.json
pip install -r requirements.txt   # reinstall previous versions
```

### 9. Report_Failure
Create a task doc for each package that couldn't be updated:
```markdown
# Task: Update <package> from <old> to <new>
**Status:** blocked
**Reason:** Tests fail — [describe failure]
**Action needed:** [fix compatibility / wait for upstream fix / find alternative]
```

## Exit Criteria
- All security-critical packages updated or documented as blocked.
- All minor/patch updates applied and tests passing.
- Changes committed with descriptive messages.
- Blocked updates tracked as task docs.
