#!/usr/bin/env python3
"""
Continuous agent loop implementing the RPEE (Reflect-Plan-Execute-Eval) cycle.
Uses CrewAI for multi-agent orchestration.

Requirements:
    pip install crewai crewai-tools pyyaml

Usage:
    python .agent/automation/agent-loop.py --tasks "Refactor auth module" "Add rate limiting"
    python .agent/automation/agent-loop.py --cycles 5
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from crewai import Agent, Task, Crew, Process
except ImportError:
    print("CrewAI not installed. Run: pip install crewai crewai-tools")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

AGENT_DIR = Path(__file__).resolve().parent.parent
MEMORY_PATH = AGENT_DIR / "learning" / "memory.json"
REFLECTION_PATH = AGENT_DIR / "learning" / "reflection-log.md"
AGENTS_CONFIG = AGENT_DIR / "agents" / "config.yaml"


def load_config() -> dict:
    """Load multi-agent config from YAML."""
    with open(AGENTS_CONFIG) as f:
        return yaml.safe_load(f)


def build_agents(config: dict) -> dict[str, Agent]:
    """Instantiate CrewAI agents from config."""
    llm_model = config.get("llm", {}).get("model", "gpt-4.1")

    planner = Agent(
        role="Planner",
        goal="Break tasks into small, testable implementation steps.",
        backstory="Senior architect who plans minimal, safe changes.",
        llm=llm_model,
        verbose=False,
    )
    coder = Agent(
        role="Coder",
        goal="Implement code changes following the plan with minimal diff.",
        backstory="Precise engineer who respects existing code style.",
        llm=llm_model,
        verbose=False,
    )
    tester = Agent(
        role="Tester",
        goal="Validate changes via tests, linting, and type checking.",
        backstory="QA specialist focused on regressions and edge cases.",
        llm=llm_model,
        verbose=False,
    )
    reviewer = Agent(
        role="Reviewer",
        goal="Review code for bugs, security issues, and quality.",
        backstory="Senior reviewer who checks correctness and style.",
        llm=llm_model,
        verbose=False,
    )
    return {"planner": planner, "coder": coder, "tester": tester, "reviewer": reviewer}


def eval_score(result) -> float:
    """Extract a numeric score from the crew result. Placeholder logic."""
    result_str = str(result).lower()
    if "error" in result_str or "fail" in result_str:
        return 0.4
    if "partial" in result_str:
        return 0.6
    return 0.85


def log_reflection(task_desc: str, outcome: str, score: float) -> None:
    """Append a reflection entry to the reflection log."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"""
---

## {now} — {task_desc}
- **Task:** {task_desc}
- **Outcome:** {outcome} (score: {score:.2f})
- **What went well:** [Auto-generated — review and edit]
- **What failed:** [Auto-generated — review and edit]
- **Root cause:** [To be filled]
- **Improvement applied:** [To be filled]
- **Follow-up eval:** Pending
- **SOP created:** No
- **Skill evolved:** No
"""
    with open(REFLECTION_PATH, "a") as f:
        f.write(entry)


def update_memory(task_id: int, task_desc: str, outcome: str, score: float) -> None:
    """Append a task record to memory.json."""
    with open(MEMORY_PATH) as f:
        memory = json.load(f)

    memory["entries"].append({
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": task_desc,
        "domain": "general",
        "outcome": outcome,
        "score": score,
        "reflection": f"Auto-logged by agent-loop. Score={score:.2f}",
        "skills_used": [],
        "vector": [0.0] * 8,  # Placeholder — replace with real embeddings
    })

    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


def run_cycle(agents: dict, task_desc: str, task_id: int) -> float:
    """Run one RPEE cycle for a single task."""
    print(f"\n{'='*60}")
    print(f"[CYCLE {task_id}] {task_desc}")
    print(f"{'='*60}")

    # Plan
    plan_task = Task(
        description=f"Plan implementation for: {task_desc}. Output a numbered step list.",
        expected_output="A numbered implementation plan with testable steps.",
        agent=agents["planner"],
    )

    # Execute
    code_task = Task(
        description=f"Implement the plan for: {task_desc}. Output the code changes as a diff.",
        expected_output="Code diff or file changes implementing the plan.",
        agent=agents["coder"],
    )

    # Test
    test_task = Task(
        description=f"Validate the implementation of: {task_desc}. Run tests and report results.",
        expected_output="Test results: pass/fail with details.",
        agent=agents["tester"],
    )

    # Review
    review_task = Task(
        description=f"Review the code changes for: {task_desc}. Check for bugs, security, style.",
        expected_output="Review findings with severity ratings.",
        agent=agents["reviewer"],
    )

    crew = Crew(
        agents=list(agents.values()),
        tasks=[plan_task, code_task, test_task, review_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    score = eval_score(result)
    outcome = "success" if score >= 0.7 else "partial" if score >= 0.5 else "failure"

    print(f"\n[RESULT] {outcome} (score: {score:.2f})")

    # Reflect
    log_reflection(task_desc, outcome, score)
    update_memory(task_id, task_desc, outcome, score)

    # Evolve if needed
    if score < 0.7:
        print("[EVOLVE] Score below threshold — triggering skill evolution...")
        subprocess.run(
            [sys.executable, str(AGENT_DIR / "automation" / "evolve-skills.py")],
            cwd=str(AGENT_DIR.parent),
        )

    return score


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent RPEE loop")
    parser.add_argument("--tasks", nargs="+", default=["Run daily code review"], help="Task descriptions")
    parser.add_argument("--cycles", type=int, default=1, help="Number of cycles per task")
    parser.add_argument("--delay", type=int, default=5, help="Seconds between cycles")
    args = parser.parse_args()

    config = load_config()
    agents = build_agents(config)
    task_id = int(time.time())  # Simple monotonic ID

    for cycle in range(args.cycles):
        for task_desc in args.tasks:
            task_id += 1
            score = run_cycle(agents, task_desc, task_id)
            print(f"[SLEEP] Waiting {args.delay}s before next cycle...")
            time.sleep(args.delay)

    print("\n[DONE] All cycles complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())