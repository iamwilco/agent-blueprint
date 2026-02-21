# Skills Index
> Categorized, reusable operator playbooks. Each skill has a `SKILL.md` with description, usage, code snippet, and eval method. Evolve low-scoring skills via `automation/evolve-skills.py`.

## How Skills Work
1. Agent matches incoming task to a skill by category + description.
2. Agent follows the skill's procedure and code snippets.
3. Post-task, the skill is scored via its eval method.
4. Skills scoring below threshold are candidates for DGM-style evolution (mutate → eval → select best).

## Skill Catalog
| Domain | Skill | Description | Path |
|---|---|---|---|
| coding | git-commit-formatter | Conventional commit messages | `skills/coding/git-commit-formatter/SKILL.md` |
| coding | code-reviewer | Automated code review | `skills/coding/code-reviewer/SKILL.md` |
| coding | refactor-assistant | Safe, incremental refactoring | `skills/coding/refactor-assistant/SKILL.md` |
| testing | unit-testing | Isolated unit test design | `skills/testing/unit-testing/SKILL.md` |
| testing | integration-testing | Cross-boundary test design | `skills/testing/integration-testing/SKILL.md` |
| deployment | docker-build | Containerized build & deploy | `skills/deployment/docker-build/SKILL.md` |

## Adding a New Skill
1. Create `skills/<domain>/<skill-name>/SKILL.md`.
2. Follow the template: Description, Usage, Code Snippet, Eval Method.
3. Optionally add an `eval.py` for automated scoring.
4. Register it in this index table.
