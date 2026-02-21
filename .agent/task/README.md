# Task Docs
> PRDs, implementation plans, and post-task history organized by domain.

## How to Use
1. Before starting a feature, create `task/<domain>/<feature-name>.md` from the template below.
2. Fill in Context, Goal, Scope, and Plan before writing code.
3. Update Decisions and Outcome after completion.
4. Agents: check this folder before implementing similar features — prior art saves tokens.

## Task Template
```markdown
# Task: [Feature Name]
**Domain:** [e.g., auth, billing, frontend]
**Status:** draft | in-progress | done | abandoned
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

## Context
Why this task exists. Link to issue/ticket if applicable.

## Goal
One-sentence success criteria.

## Scope
- **In scope:** ...
- **Out of scope:** ...

## Plan
1. Step one (est. X hours)
2. Step two
3. ...

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| API breaking change | Medium | Version the endpoint |

## Decisions
| Decision | Rationale | Date |
|---|---|---|
| Use JWT over sessions | Stateless scaling | YYYY-MM-DD |

## Outcome
- Result:
- Metrics:
- Follow-up tasks:
- Reflection logged: [link to learning/reflection-log.md entry]
```

## Index
| Domain | Doc | Status | Last Updated |
|---|---|---|---|
| auth | `task/auth/example-auth.md` | done | 2025-01-22 |

## Repeating Tasks
Agents can auto-schedule these. Add new ones below:
| Task | Frequency | Trigger | Last Run |
|---|---|---|---|
| Daily code review | daily | `workflows/code-review.md` | — |
| Dependency audit | weekly | `update.md` step 6 | — |
| Skill evolution cycle | weekly | `automation/evolve-skills.py` | — |
