# Agent Blueprint

A modular, self-evolving `.agent` folder structure for AI-assisted coding projects. Drop it into any repo to give AI agents persistent context, reusable skills, autonomous workflows, and a self-improvement loop inspired by Darwin Gödel Machines (DGM) and Group-Evolving Agents (GEA).

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [What's Inside](#whats-inside)
3. [How to Use — Step by Step](#how-to-use--step-by-step)
   - [Scenario A: Starting a Brand-New Project](#scenario-a-starting-a-brand-new-project)
   - [Scenario B: Adding the Blueprint to an Existing Project](#scenario-b-adding-the-blueprint-to-an-existing-project)
   - [Scenario C: Turning an Idea Into a Working Project](#scenario-c-turning-an-idea-into-a-working-project)
   - [Scenario D: Daily Development Workflow](#scenario-d-daily-development-workflow)
4. [Go-To Prompts Reference](#go-to-prompts-reference)
5. [Core Concepts](#core-concepts)
6. [Automation & Maintenance](#automation--maintenance)
7. [Customization](#customization)
8. [Contributing](#contributing)

---

## Quick Start

```bash
# 1. Clone this blueprint
git clone git@github.com:iamwilco/agent-blueprint.git

# 2. Copy .agent into your project
cp -r agent-blueprint/.agent /path/to/your-project/

# 3. Initialize for your project (paste initialize.md as a prompt to your AI agent)
#    -> Feed this to Claude, Windsurf, Cursor, Copilot, or any AI coding assistant.
```

---

## What's Inside

```
.agent/
├── README.md              # Navigation index, project overview, tech stack
├── initialize.md          # Prompt: tailor blueprint to a new project
├── update.md              # Prompt: sync/update blueprint for existing project
├── system/                # Architecture, schemas, API contracts
├── task/                  # PRDs, plans, implementation history by domain
├── SOPs/                  # Repeatable procedures from resolved issues
├── skills/                # Categorized, reusable operator playbooks
├── workflows/             # Graph-based step-by-step guides (build, test, deploy, self-improve)
├── guidelines/            # Agent behavior rules and model-specific tips
├── learning/              # Memory store, evals, reflection logs for self-improvement
├── automation/            # Scripts: agent loops, skill evolution, git hooks
└── agents/                # Multi-agent YAML configs (planner, coder, tester, reviewer)
```

---

## How to Use — Step by Step

### Scenario A: Starting a Brand-New Project

You have an idea and want to start a new repo from scratch with full AI agent support.

**Step 1 — Create your project and copy the blueprint**
```bash
mkdir my-new-project && cd my-new-project
git init
cp -r /path/to/agent-blueprint/.agent .
```

**Step 2 — Open `initialize.md` and give it to your AI agent**

Open `.agent/initialize.md` in your editor. This file is a prompt that tells the AI agent how to configure the entire `.agent/` folder for your specific project. Copy-paste it into your AI assistant (Windsurf Cascade, Cursor, Claude, ChatGPT, etc.) along with a description of your project:

```
Prompt to paste:
─────────────────────────────────────────────────
Read the file .agent/initialize.md and follow its instructions.

Here is my project:
- Name: [Your Project Name]
- Description: [What it does in 2-3 sentences]
- Tech stack: [e.g., Python FastAPI backend, React frontend, PostgreSQL, Redis, Docker]
- Key features: [e.g., user auth, real-time notifications, payment processing]
─────────────────────────────────────────────────
```

**What the agent does:**
1. Scans your project (README, `package.json`, `requirements.txt`, git log).
2. Rewrites `.agent/README.md` with your actual tech stack and module diagram.
3. Populates `system/architecture.md`, `database-schema.md`, `api-endpoints.md` for your project.
4. Adds project-specific skills and workflows.
5. Initializes `learning/memory.json` as empty, ready for your first task.
6. Validates everything is consistent.

**Step 3 — Start building**

Now use the agent to implement features. See [Scenario C](#scenario-c-turning-an-idea-into-a-working-project) and [Go-To Prompts](#go-to-prompts-reference) below.

---

### Scenario B: Adding the Blueprint to an Existing Project

You already have a codebase and want to add AI agent context to it.

**Step 1 — Copy the blueprint into your repo**
```bash
cd /path/to/your-existing-project
cp -r /path/to/agent-blueprint/.agent .
```

**Step 2 — Open `update.md` and give it to your AI agent**

This prompt tells the agent to analyze your existing project and adapt the blueprint:

```
Prompt to paste:
─────────────────────────────────────────────────
Read the file .agent/update.md and follow its instructions.

This is an existing project. Analyze the codebase and update the .agent/
folder to match the current state of the project. Focus on:
- system/architecture.md — map our actual components and data flows
- system/database-schema.md — document our actual DB schema
- system/api-endpoints.md — document our actual API routes
- .agent/README.md — fill in our real tech stack and modules
─────────────────────────────────────────────────
```

**What the agent does:**
1. Reads your source files, configs, and git history.
2. Fills in `system/` docs with your real architecture, schema, and APIs.
3. Updates the tech stack table and dependency diagram.
4. Identifies which skills and workflows are relevant to your stack.
5. Runs a self-improvement check and logs the initial state.

**Step 3 — Commit the initialized `.agent/` folder**
```bash
git add .agent/
git commit -m "chore(agent): initialize agent blueprint for existing project"
```

---

### Scenario C: Turning an Idea Into a Working Project

This is the most powerful pattern: you have an idea in your head and you want the AI agent to plan, build, test, and iterate on it autonomously.

**Step 1 — Write a task document**

Create a file in `.agent/task/` describing what you want:

```
Prompt to paste:
─────────────────────────────────────────────────
I want to build [describe your idea]. Create a task document at
.agent/task/[domain]/[task-name].md using the template from
.agent/task/README.md. Include:

- Context: Why this feature matters
- Goal: What "done" looks like
- Scope: What's included and excluded
- Plan: Step-by-step implementation plan
- Risks: What could go wrong
─────────────────────────────────────────────────
```

**Step 2 — Have the agent implement it step by step**

```
Prompt to paste:
─────────────────────────────────────────────────
Read .agent/task/[domain]/[task-name].md and implement it.

Follow these guidelines:
- Read .agent/guidelines/agent-behavior.md for behavior rules
- Use skills from .agent/skills/ that match this task
- Follow the workflow in .agent/workflows/build.md for building
- Follow .agent/workflows/test.md for testing
- Commit with conventional format: type(scope): description
─────────────────────────────────────────────────
```

**Step 3 — Review the implementation**

```
Prompt to paste:
─────────────────────────────────────────────────
Run the code review workflow from .agent/workflows/code-review.md
on the changes you just made. Use the checklist from
.agent/skills/coding/code-reviewer/SKILL.md.
─────────────────────────────────────────────────
```

**Step 4 — Reflect and improve**

```
Prompt to paste:
─────────────────────────────────────────────────
The task is complete. Follow the self-improvement workflow:
1. Append a reflection to .agent/learning/reflection-log.md
2. Update .agent/learning/memory.json with this task
3. If you discovered a reusable pattern, propose a new skill in .agent/skills/
4. If you resolved a tricky issue, propose an SOP in .agent/SOPs/
─────────────────────────────────────────────────
```

---

### Scenario D: Daily Development Workflow

Once the blueprint is set up, here's how you use it day-to-day.

**Before starting work — context load**
```
Prompt to paste:
─────────────────────────────────────────────────
Read .agent/README.md to understand the project. Then read
.agent/learning/reflection-log.md for recent context.
I want to work on: [describe what you want to do today]
─────────────────────────────────────────────────
```

**While coding — use skills as needed**
```
Prompt to paste:
─────────────────────────────────────────────────
I need to [write tests / refactor / review / deploy].
Read the relevant skill from .agent/skills/ and apply it:
- Testing: .agent/skills/testing/unit-testing/SKILL.md
- Refactoring: .agent/skills/coding/refactor-assistant/SKILL.md
- Code review: .agent/skills/coding/code-reviewer/SKILL.md
- Docker/deploy: .agent/skills/deployment/docker-build/SKILL.md
─────────────────────────────────────────────────
```

**Before committing — format the commit**
```
Prompt to paste:
─────────────────────────────────────────────────
Read .agent/skills/coding/git-commit-formatter/SKILL.md.
Format a commit message for these changes: [describe changes]
─────────────────────────────────────────────────
```

**End of day — reflect**
```
Prompt to paste:
─────────────────────────────────────────────────
Summarize what we accomplished today and append a reflection to
.agent/learning/reflection-log.md using the template at the bottom
of that file.
─────────────────────────────────────────────────
```

---

## Go-To Prompts Reference

Copy-paste these directly into your AI coding assistant. Replace `[bracketed]` parts with your specifics.

### Project Setup Prompts

| When | Prompt |
|---|---|
| **New project** | `Read .agent/initialize.md and follow its instructions. My project: [name], [tech stack], [description].` |
| **Existing project** | `Read .agent/update.md and follow its instructions. Analyze the codebase and update .agent/ to match.` |
| **Sync blueprint updates** | `Run .agent/automation/sync-from-template.sh --dry-run and show me what would change.` |

### Task & Feature Prompts

| When | Prompt |
|---|---|
| **Plan a new feature** | `Create a task document at .agent/task/[domain]/[name].md using the template from .agent/task/README.md for: [describe feature]` |
| **Implement a task** | `Read .agent/task/[domain]/[name].md and implement it step by step. Follow .agent/guidelines/agent-behavior.md.` |
| **Break down a big idea** | `I want to build [idea]. Break it into 5-8 small tasks, each independently testable. Create task docs for each in .agent/task/[domain]/.` |
| **Debug an issue** | `I'm seeing [error]. Read .agent/system/architecture.md for context, diagnose the root cause, and suggest a minimal fix.` |

### Quality & Review Prompts

| When | Prompt |
|---|---|
| **Code review** | `Follow .agent/workflows/code-review.md on the current staged changes.` |
| **Write tests** | `Read .agent/skills/testing/unit-testing/SKILL.md and write tests for [module/function].` |
| **Integration tests** | `Read .agent/skills/testing/integration-testing/SKILL.md and write integration tests for [endpoint/flow].` |
| **Refactor** | `Read .agent/skills/coding/refactor-assistant/SKILL.md and refactor [module] to [reduce complexity / extract class / etc].` |
| **Debug an error** | `Read .agent/skills/debugging/error-handling/SKILL.md. I'm seeing [error]. Diagnose root cause and fix at source.` |
| **Optimize performance** | `Read .agent/skills/optimization/performance-tuning/SKILL.md. [endpoint/query] is slow — profile, find bottleneck, fix, measure.` |

### Build & Deploy Prompts

| When | Prompt |
|---|---|
| **Build** | `Follow .agent/workflows/build.md to build the project. Report any issues.` |
| **Test** | `Follow .agent/workflows/test.md. Run fast tests first, then full suite.` |
| **Deploy** | `Follow .agent/workflows/deploy.md to deploy to [staging/production].` |
| **Docker** | `Read .agent/skills/deployment/docker-build/SKILL.md and create/update the Dockerfile.` |
| **Update deps** | `Follow .agent/workflows/dependency-update.md to audit and update dependencies.` |

### Learning & Self-Improvement Prompts

| When | Prompt |
|---|---|
| **Post-task reflection** | `Append a reflection to .agent/learning/reflection-log.md for: [what we just did].` |
| **Run benchmarks** | `Run python .agent/learning/evals/coding-bench.py and report results.` |
| **Evolve skills** | `Run python .agent/automation/evolve-skills.py --all and report which skills improved.` |
| **Self-improve loop** | `Follow .agent/workflows/self-improve.md to identify weaknesses and evolve.` |
| **Create new skill** | `I noticed a reusable pattern for [X]. Create a new skill at .agent/skills/[domain]/[name]/SKILL.md following the format of existing skills.` |
| **Create new SOP** | `We just solved [tricky issue]. Create an SOP at .agent/SOPs/[category]/[name].md using the template from .agent/SOPs/README.md.` |

### Multi-Agent Prompts (Advanced)

| When | Prompt |
|---|---|
| **Full autonomous cycle** | `Run python .agent/automation/agent-loop.py --tasks "[task1]" "[task2]" --cycles 3` |
| **Review agent config** | `Read .agent/agents/config.yaml and suggest improvements for our workflow.` |
| **Add a new agent role** | `Create a new agent YAML at .agent/agents/[role].yaml following the format of existing agents. Role: [description].` |

---

## Core Concepts

- **Reflection-Plan-Execute-Eval (RPEE) Loop** — Agents reflect on past tasks, plan next steps, execute changes, and evaluate results. Logged in `learning/reflection-log.md`.
- **Skill Evolution (DGM-inspired)** — `automation/evolve-skills.py` generates skill variants, benchmarks them, and promotes the best. Self-modifying within safety constraints.
- **Group Evolution (GEA-inspired)** — Multiple agents (planner, coder, tester, reviewer) collaborate and co-evolve strategies via shared memory in `learning/memory.json`.
- **Vector Memory** — `learning/memory.json` stores task embeddings for retrieval-augmented generation, enabling agents to recall similar past tasks.
- **SWE-bench Evals** — `learning/evals/` contains benchmark scripts to measure skill quality against real-world coding tasks.

---

## Automation & Maintenance

### Repeating Tasks (add to your calendar or cron)

| Task | Frequency | Command / Prompt |
|---|---|---|
| **Code review** | Daily | Paste: `Follow .agent/workflows/code-review.md on changes since yesterday.` |
| **Run benchmarks** | Weekly | `python .agent/learning/evals/coding-bench.py` |
| **Evolve skills** | Weekly | `python .agent/automation/evolve-skills.py --all` |
| **Sync blueprint** | Monthly | `bash .agent/automation/sync-from-template.sh` |
| **Reflection review** | Weekly | Paste: `Read .agent/learning/reflection-log.md and summarize patterns. Suggest improvements.` |

### Git Hook (automatic)

Install the post-commit hook to auto-log every commit to memory:
```bash
ln -sf ../../.agent/automation/git-hooks/post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

---

## Customization

- **Add domain-specific skills** — Create folders under `skills/` (e.g., `ml/`, `mobile/`, `devops/`) with `SKILL.md` + optional `eval.py`.
- **Add project-specific workflows** — Create new `.md` files in `workflows/` (e.g., `migrate-db.md`, `release.md`).
- **Change LLM provider** — Edit `agents/config.yaml`: set `llm.provider` to `openai`, `anthropic`, or `local`, and update the model name.
- **Add new agent roles** — Create a new YAML in `agents/` following the format of `planner.yaml`.
- **Customize behavior** — Edit `guidelines/agent-behavior.md` to add project-specific rules.

---

## Contributing
1. Fork this repo.
2. Add/improve skills, workflows, or automation scripts.
3. Run evals in `learning/evals/` to validate improvements.
4. Submit a PR with benchmark results.

## License
MIT — use freely, adapt to your needs.
