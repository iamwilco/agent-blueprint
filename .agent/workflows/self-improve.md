# Self-Improve Workflow
**Trigger:** `/self-improve`

> Implements a Reflection-Plan-Execute-Eval (RPEE) loop inspired by Darwin Gödel Machines (DGM) for self-modification within safety constraints, and Group-Evolving Agents (GEA) for collaborative skill evolution.

## Graph
```
[START] → reflect → identify_weakness → plan_improvement
  → generate_variants → evaluate_variants → {best > current?}
    → promote_variant → update_memory → log_reflection → [END]
    → discard_variants → log_reflection → [END]
```

## LangGraph Pseudocode
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ImprovementState(TypedDict):
    reflection: str           # What went wrong / what to improve
    weakness: str             # Identified skill or SOP gap
    variants: list[dict]      # Generated improvement candidates
    scores: list[float]       # Eval scores per variant
    best_variant: dict | None # Selected improvement
    promoted: bool            # Whether improvement was adopted

def reflect(state: ImprovementState) -> ImprovementState:
    """Analyze learning/reflection-log.md and learning/memory.json for patterns."""
    # Parse recent reflections for repeated failures
    # Query memory.json for similar past tasks with low scores
    state["reflection"] = "Repeated test failures in auth module"
    return state

def identify_weakness(state: ImprovementState) -> ImprovementState:
    """Map reflection to a specific skill or SOP that needs improvement."""
    # Cross-reference failure pattern with skills/README.md
    state["weakness"] = "skills/testing/unit-testing/SKILL.md"
    return state

def plan_improvement(state: ImprovementState) -> ImprovementState:
    """Design 3 variant improvements (DGM: self-modify within constraints)."""
    # Variant 1: Add edge case checklist item
    # Variant 2: Rewrite code snippet with better mock patterns
    # Variant 3: Add new eval metric (mutation testing)
    state["variants"] = [{"id": i, "description": f"variant_{i}"} for i in range(3)]
    return state

def evaluate_variants(state: ImprovementState) -> ImprovementState:
    """Score each variant against evals (GEA: collaborative evaluation)."""
    # Run learning/evals/coding-bench.py for each variant
    # Score = weighted(correctness * 0.4 + efficiency * 0.3 + coverage * 0.3)
    state["scores"] = [0.72, 0.85, 0.78]
    state["best_variant"] = state["variants"][1]  # Highest score
    return state

def should_promote(state: ImprovementState) -> str:
    """Gate: only promote if best variant scores higher than current baseline."""
    current_baseline = 0.75  # From last eval run
    if max(state["scores"]) > current_baseline:
        return "promote"
    return "discard"

def promote_variant(state: ImprovementState) -> ImprovementState:
    """Write the improved skill/SOP back to disk."""
    # Overwrite the SKILL.md with best variant content
    # Increment version number
    state["promoted"] = True
    return state

def update_memory(state: ImprovementState) -> ImprovementState:
    """Store improvement record in learning/memory.json."""
    # Append: {task_id, description, outcome, score, vector}
    return state

def log_reflection(state: ImprovementState) -> ImprovementState:
    """Append entry to learning/reflection-log.md."""
    return state

# Build graph
graph = StateGraph(ImprovementState)
graph.add_node("reflect", reflect)
graph.add_node("identify_weakness", identify_weakness)
graph.add_node("plan_improvement", plan_improvement)
graph.add_node("evaluate_variants", evaluate_variants)
graph.add_node("promote_variant", promote_variant)
graph.add_node("update_memory", update_memory)
graph.add_node("log_reflection", log_reflection)

graph.set_entry_point("reflect")
graph.add_edge("reflect", "identify_weakness")
graph.add_edge("identify_weakness", "plan_improvement")
graph.add_edge("plan_improvement", "evaluate_variants")
graph.add_conditional_edges("evaluate_variants", should_promote, {
    "promote": "promote_variant",
    "discard": "log_reflection",
})
graph.add_edge("promote_variant", "update_memory")
graph.add_edge("update_memory", "log_reflection")
graph.add_edge("log_reflection", END)

app = graph.compile()
```

## Safety Constraints (DGM-inspired)
- **No destructive writes** without passing eval threshold first.
- **Version skills** — never overwrite without incrementing version.
- **Rollback** — keep previous version; revert if post-promotion eval drops.
- **Audit trail** — every promotion logged in `reflection-log.md` with before/after scores.
