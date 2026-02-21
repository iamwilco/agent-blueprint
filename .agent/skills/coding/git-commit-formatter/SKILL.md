# Skill: Git Commit Formatter
**Domain:** coding
**Version:** 1.1
**Eval Score:** 0.78

## Description
Generate clear, scoped commit messages following [Conventional Commits](https://www.conventionalcommits.org/). Ensures consistent git history for changelogs, semantic versioning, and agent traceability.

## Usage
1. Analyze the staged diff (`git diff --cached --stat`).
2. Identify primary change type: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`.
3. Determine scope from the most-affected module or directory.
4. Write subject line ≤72 chars; imperative mood.
5. Add body bullets for non-trivial changes (what + why, not how).
6. Append footer for breaking changes or issue refs.

## Code Snippet
```python
def format_commit(change_type: str, scope: str, subject: str, body: list[str] = None, breaking: bool = False, issue: str = None) -> str:
    prefix = f"{'!' if breaking else ''}"
    header = f"{change_type}({scope}){prefix}: {subject}"
    lines = [header, ""]
    if body:
        lines.extend(f"- {b}" for b in body)
        lines.append("")
    if breaking:
        lines.append("BREAKING CHANGE: see migration guide.")
    if issue:
        lines.append(f"Closes {issue}")
    return "\n".join(lines)
```

## Output Template
```
feat(auth): add JWT refresh token rotation

- Add /auth/refresh endpoint
- Store refresh token family for reuse detection
- Expire old tokens on rotation

Closes #142
```

## Eval Method
- **Metric:** Conventional Commits compliance rate.
- **Test:** Parse 20 recent commits; check regex `^(feat|fix|docs|refactor|test|chore|perf|ci)\(.+\): .{1,72}$`.
- **Threshold:** ≥90% compliance = pass.
