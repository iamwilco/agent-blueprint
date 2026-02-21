# Code Review Workflow
**Trigger:** `/review`

## Graph
```
[START] → gather_diff → static_analysis → llm_review
  → synthesize_findings → {critical_found?}
    → block_with_findings → [END]
    → approve_with_suggestions → [END]
```

## Nodes

### 1. gather_diff
```bash
git diff --cached --stat
git diff --cached
```
Collect: changed files, insertions, deletions, affected modules.

### 2. static_analysis
Run automated checks in parallel:
```bash
ruff check $(git diff --cached --name-only --diff-filter=ACMR -- '*.py')
mypy $(git diff --cached --name-only --diff-filter=ACMR -- '*.py')
# Node.js: eslint --no-error-on-unmatched-pattern $(git diff ...)
```
Collect structured output (file, line, rule, message).

### 3. llm_review
Apply `skills/coding/code-reviewer/SKILL.md` checklist to each changed file:
- Correctness, security, error handling, test coverage, performance, style, backward compat.
- Output findings as structured JSON: `{severity, file, line, description, suggestion}`.

### 4. synthesize_findings
Merge static analysis + LLM findings. Deduplicate. Sort by severity (critical > warning > info).

Output format:
```
## Review Summary
- **Critical:** N findings (must fix)
- **Warning:** N findings (should fix)
- **Info:** N findings (optional)

### Critical
1. [file:line] description — suggestion

### Warning
1. [file:line] description — suggestion
```

### 5. block_with_findings
If any critical findings: output review with `CHANGES REQUESTED` status. Do not auto-merge.

### 6. approve_with_suggestions
If no critical findings: output review with `APPROVED` status + optional suggestions.

## Post-Review
- Log review stats to `learning/memory.json` (files reviewed, findings count, time).
- If same finding type appears 3+ times across reviews → trigger `workflows/self-improve.md` to create a new SOP or skill.
