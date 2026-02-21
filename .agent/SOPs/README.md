# Standard Operating Procedures (SOPs)
> Auto-generated from resolved issues. Agents: after fixing a non-trivial bug or setting up an integration, create an SOP so the fix is never re-discovered from scratch.

## When to Create an SOP
- A bug took >30 min to diagnose.
- A setup/integration required >3 non-obvious steps.
- A `fix:` commit appears in git log for the same area twice.

## SOP Template
```markdown
# SOP: [Short Title]
**Category:** [e.g., integrations, debugging, deployment, database]
**Created:** YYYY-MM-DD
**Last Verified:** YYYY-MM-DD

## Problem Statement
One sentence: what goes wrong and when.

## Preconditions
- Environment requirements (OS, runtime version, env vars).
- Services that must be running.

## Procedure
1. Step one — command or action.
2. Step two — expected output.
3. ...

## Validation
- [ ] Check 1: [how to confirm success]
- [ ] Check 2: [how to confirm no side-effects]

## Rollback
If the procedure fails midway:
1. Undo step N.
2. Restore from backup / revert commit.

## References
- Related issue/PR: [link]
- Related task doc: [link to task/domain/...]
```

## Index
| Category | SOP | Trigger | Last Verified |
|---|---|---|---|
| debugging | `SOPs/debugging/flaky-test-fix.md` | Test suite flake | YYYY-MM-DD |
| deployment | `SOPs/deployment/rollback-procedure.md` | Failed deploy | YYYY-MM-DD |
| integrations | `SOPs/integrations/third-party-api-setup.md` | New integration | YYYY-MM-DD |
