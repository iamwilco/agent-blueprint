# Workflows Index
> Graph-based operational guides for agents. Each workflow defines a trigger, a node graph (steps), conditional edges, and exit criteria. Compatible with LangGraph/CrewAI execution.

## Workflow Catalog
| Trigger | Workflow | Description | Path |
|---|---|---|---|
| `/build` | Build | Compile, bundle, report errors | `workflows/build.md` |
| `/test` | Test | Run test suites, summarize failures | `workflows/test.md` |
| `/deploy` | Deploy | Build image, push, deploy to target | `workflows/deploy.md` |
| `/review` | Code Review | Structured review of staged changes | `workflows/code-review.md` |
| `/self-improve` | Self-Improve | RPEE loop for agent evolution | `workflows/self-improve.md` |
| `/deps-update` | Dependency Update | Audit, update, and validate dependencies | `workflows/dependency-update.md` |

## Workflow Graph Convention
Each workflow uses this pseudocode format:
```
[START] → Node_A → {condition} → Node_B | Node_C → [END]
```
- **Nodes** = actions (build, test, review, reflect).
- **Edges** = transitions, optionally conditional (`{if tests_pass}`).
- **State** = shared dict passed between nodes (LangGraph `TypedDict` pattern).
