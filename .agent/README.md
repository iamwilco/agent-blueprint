# 📚 Agent Blueprint — Internal Documentation

> This file is the agent's entry point. When you paste a prompt like _"Read .agent/README.md"_, the AI reads this first to understand your project, tech stack, and where everything lives.

---

## Quick Navigation

| Folder | Purpose | When to Read |
|---|---|---|
| `system/` | Architecture, schemas, API contracts | First — for design decisions and data flows |
| `task/` | PRDs, plans, implementation history | Before similar features; update post-task |
| `SOPs/` | Repeatable procedures from resolved issues | For known issues; auto-generate new ones post-fix |
| `skills/` | Categorized reusable operators/playbooks | Match skill to task type; evolve via `automation/evolve-skills.py` |
| `workflows/` | Graph-based operational guides | Execute task workflows; trigger `/self-improve` for evolution |
| `guidelines/` | Agent behavior rules, model tips | Always — enforce token efficiency and best practices |
| `learning/` | Memory, evals, reflection logs | Post-task reflection; run evals to score improvements |
| `automation/` | Loop scripts, sync, git hooks | For continuous cycles; run `agent-loop.py` for autonomy |
| `agents/` | Multi-agent YAML configs | Orchestrate via CrewAI/LangGraph |

---

## How to Use This Folder

### For Humans (you)
You interact with the `.agent/` folder by **giving prompts to your AI coding assistant** (Windsurf, Cursor, Claude, Copilot, etc.) that reference these files. The AI reads the docs and follows the instructions inside them.

**You never need to edit these files manually** — the AI does it. Your job is to:
1. Describe what you want.
2. Point the AI to the right file.
3. Review what it produces.

### For AI Agents
When referenced, these files provide:
- **Context** — architecture, schemas, APIs so you don't have to re-explain.
- **Skills** — step-by-step procedures for common tasks (testing, reviewing, deploying).
- **Workflows** — multi-step graphs for complex operations.
- **Memory** — past task outcomes to avoid repeating mistakes.

---

## Common Workflows (copy-paste these prompts)

### "I have a new idea — build it for me"
```
1. Create a task document:
   "I want to build [your idea]. Create a task doc at .agent/task/[domain]/[name].md
    using the template from .agent/task/README.md."

2. Implement it:
   "Read .agent/task/[domain]/[name].md and implement it step by step.
    Follow .agent/guidelines/agent-behavior.md."

3. Review it:
   "Follow .agent/workflows/code-review.md on the changes."

4. Reflect:
   "Append a reflection to .agent/learning/reflection-log.md."
```

### "I need to fix a bug"
```
"I'm seeing [error/behavior]. Read .agent/system/architecture.md for context.
 Diagnose the root cause and suggest a minimal fix.
 Follow .agent/skills/coding/code-reviewer/SKILL.md for review."
```

### "Write tests for this module"
```
"Read .agent/skills/testing/unit-testing/SKILL.md and write tests for [module].
 Use the AAA pattern. Target edge cases and error paths."
```

### "Refactor this code"
```
"Read .agent/skills/coding/refactor-assistant/SKILL.md and refactor [module/file]
 to reduce complexity. Keep all tests passing."
```

### "Deploy this"
```
"Follow .agent/workflows/deploy.md to deploy to [staging/production].
 Read .agent/skills/deployment/docker-build/SKILL.md for Docker best practices."
```

### "Start of day — load context"
```
"Read .agent/README.md and .agent/learning/reflection-log.md for recent context.
 I want to work on [today's task]."
```

### "End of day — reflect"
```
"Summarize what we accomplished today and append a reflection to
 .agent/learning/reflection-log.md using the template."
```

---

## Project Overview

<!-- ═══════════════════════════════════════════════════════════════════
     AUTO-POPULATED: The sections below are filled in by the AI agent
     when you run initialize.md (new project) or update.md (existing).
     The example content below is a generic placeholder.
     ═══════════════════════════════════════════════════════════════════ -->

**Example:** A Python Flask backend with a React frontend, PostgreSQL database, and Redis cache. Deployed via Docker on AWS ECS.

## Technology Stack

| Layer | Technology | Key Modules |
|---|---|---|
| Backend | Python / Flask | `api-server`, `worker` |
| Frontend | React / TypeScript | `web-ui` |
| Database | PostgreSQL | migrations via Alembic |
| Cache | Redis | session + queue |
| Infra | Docker / AWS ECS | `Dockerfile`, `docker-compose.yml` |

## Module Dependencies

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ web-ui   │────▶│api-server│────▶│PostgreSQL│
│ (React)  │     │ (Flask)  │────▶│  Redis   │
└──────────┘     └────┬─────┘     └──────────┘
                      │
                 ┌────▼─────┐
                 │  worker   │
                 │(Celery)   │
                 └───────────┘
```

## Quick Commands

```bash
docker compose build          # Build
pytest tests/ --cov=src       # Test
ruff check src/ && mypy src/  # Lint
docker compose up -d           # Dev server
```