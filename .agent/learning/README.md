# Learning & Self-Improvement
> Agents evolve through structured feedback loops. This folder is the engine.

## How Agents Learn
| Mechanism | File/Folder | Description |
|---|---|---|
| Reflection | `reflection-log.md` | Post-task log: what worked, what failed, root cause, improvement |
| Memory (RAG) | `memory.json` | Vector store of past tasks for retrieval-augmented generation |
| Evals | `evals/` | Benchmark scripts to score skill quality objectively |
| Evolution | `../automation/evolve-skills.py` | DGM-inspired: mutate skills, eval variants, promote best |

## Learning Cycle
```
Task Complete → Reflect (log outcome) → Store in Memory (embed task)
  → Run Evals (score skills) → Evolve (mutate low scorers)
  → Promote (update SKILL.md) → Next Task (with improved skills)
```

## Key Concepts
- **DGM (Darwin Gödel Machine):** Self-modifying agent that rewrites its own skills within provable safety bounds. Changes are only promoted if eval scores improve.
- **GEA (Group-Evolving Agents):** Multiple agent variants collaborate and compete. Best strategies propagate across the group.
- **RPEE Loop:** Reflect → Plan → Execute → Eval. The core cycle for continuous improvement.
- **Vector Memory:** Each task is embedded and stored in `memory.json`. Before starting a new task, the agent queries for similar past tasks to reuse successful strategies.

## Eval Scripts
| Script | What It Measures | Command |
|---|---|---|
| `evals/coding-bench.py` | Code correctness + style compliance | `python evals/coding-bench.py` |
| `evals/lint-check.py` | Lint quality across the codebase | `python evals/lint-check.py --path src/` |

## Triggers
- **Manual:** Run `workflows/self-improve.md` or `automation/agent-loop.py`.
- **Automatic:** `automation/git-hooks/post-commit` logs every commit to memory.
- **Scheduled:** Add `evolve-skills.py --all` to cron for weekly evolution cycles.