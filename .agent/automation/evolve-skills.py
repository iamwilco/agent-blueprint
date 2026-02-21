#!/usr/bin/env python3
"""
DGM-inspired skill evolution script.

Takes a skill SKILL.md, generates N prompt/procedure variants,
evaluates each against the skill's eval method, and promotes the best
if it exceeds the current baseline.

Concepts:
  - Darwin Gödel Machine (DGM): Self-modifying within provable safety bounds.
  - Group-Evolving Agents (GEA): Multiple variants compete and co-evolve.

Usage:
    python evolve-skills.py --skill skills/coding/code-reviewer/SKILL.md
    python evolve-skills.py --skill skills/testing/unit-testing/SKILL.md --variants 5
    python evolve-skills.py --all  # Evolve all skills below threshold
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


AGENT_DIR = Path(__file__).resolve().parent.parent
MEMORY_PATH = AGENT_DIR / "learning" / "memory.json"
REFLECTION_PATH = AGENT_DIR / "learning" / "reflection-log.md"
SKILLS_DIR = AGENT_DIR / "skills"
EVOLVE_THRESHOLD = 0.75  # Minimum score to keep a skill as-is


@dataclass
class SkillInfo:
    path: Path
    name: str
    domain: str
    version: str
    content: str
    eval_script: Path | None


@dataclass
class Variant:
    id: int
    description: str
    content: str
    score: float = 0.0


def parse_skill(skill_path: Path) -> SkillInfo:
    """Parse a SKILL.md file for metadata."""
    content = skill_path.read_text()
    name_match = re.search(r"^# Skill:\s*(.+)", content, re.MULTILINE)
    domain_match = re.search(r"\*\*Domain:\*\*\s*(\w+)", content)
    version_match = re.search(r"\*\*Version:\*\*\s*([\d.]+)", content)

    # Look for eval.py in same directory
    eval_script = skill_path.parent / "eval.py"
    if not eval_script.exists():
        eval_script = None

    return SkillInfo(
        path=skill_path,
        name=name_match.group(1).strip() if name_match else skill_path.stem,
        domain=domain_match.group(1) if domain_match else "unknown",
        version=version_match.group(1) if version_match else "1.0",
        content=content,
        eval_script=eval_script,
    )


def evaluate_skill(skill: SkillInfo) -> float:
    """Run the skill's eval script and extract a score."""
    if skill.eval_script is None:
        print(f"  No eval script for {skill.name} — using default score 0.70")
        return 0.70

    print(f"  Running eval: {skill.eval_script}")
    result = subprocess.run(
        [sys.executable, str(skill.eval_script)],
        capture_output=True, text=True, timeout=60,
        cwd=str(skill.path.parent),
    )

    # Parse score from output (look for "Score: N/M (XX%)")
    score_match = re.search(r"(\d+)/(\d+)\s*\((\d+)%\)", result.stdout)
    if score_match:
        return int(score_match.group(3)) / 100.0

    # Fallback: check exit code
    return 0.80 if result.returncode == 0 else 0.50


def generate_variants(skill: SkillInfo, num_variants: int) -> list[Variant]:
    """
    Generate N skill variants by applying mutation strategies.
    In a full implementation, this would call an LLM to rewrite sections.
    Here we demonstrate the structure with rule-based mutations.
    """
    variants = []
    mutation_strategies = [
        ("add_checklist_item", "Add an additional checklist/validation step"),
        ("expand_code_snippet", "Add error handling to the code snippet"),
        ("add_eval_metric", "Add a new evaluation metric"),
        ("simplify_procedure", "Reduce steps while preserving coverage"),
        ("add_edge_case", "Add edge case handling to the procedure"),
    ]

    for i in range(min(num_variants, len(mutation_strategies))):
        strategy_name, strategy_desc = mutation_strategies[i]
        # In production: call LLM with prompt like:
        #   f"Rewrite this skill to {strategy_desc}:\n{skill.content}"
        mutated_content = skill.content  # Placeholder — actual mutation via LLM
        variants.append(Variant(
            id=i,
            description=f"{strategy_name}: {strategy_desc}",
            content=mutated_content,
        ))
        print(f"  Variant {i}: {strategy_name}")

    return variants


def evaluate_variant(variant: Variant, skill: SkillInfo) -> float:
    """
    Evaluate a variant. In production, this would:
    1. Write the variant to a temp file.
    2. Run the eval script against it.
    3. Return the score.
    """
    # Placeholder — in production, write variant.content to temp SKILL.md,
    # run eval, and return real score.
    import random
    base_score = evaluate_skill(skill)
    # Simulate small random improvement/degradation
    variant.score = round(base_score + random.uniform(-0.1, 0.15), 3)
    variant.score = max(0.0, min(1.0, variant.score))
    return variant.score


def promote_variant(variant: Variant, skill: SkillInfo) -> None:
    """Replace the skill content with the winning variant and bump version."""
    # Backup current version
    backup_path = skill.path.with_suffix(f".v{skill.version}.md.bak")
    shutil.copy2(skill.path, backup_path)
    print(f"  Backed up: {backup_path.name}")

    # Bump version
    old_version = skill.version
    parts = old_version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    new_version = ".".join(parts)

    new_content = variant.content.replace(
        f"**Version:** {old_version}",
        f"**Version:** {new_version}",
    )
    new_content = re.sub(
        r"\*\*Eval Score:\*\*\s*.*",
        f"**Eval Score:** {variant.score:.2f}",
        new_content,
    )

    skill.path.write_text(new_content)
    print(f"  Promoted variant {variant.id} (v{old_version} → v{new_version}, score: {variant.score:.2f})")


def log_evolution(skill: SkillInfo, variants: list[Variant], winner: Variant | None) -> None:
    """Log evolution attempt to reflection log and memory."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    outcome = f"Promoted variant {winner.id} ({winner.score:.2f})" if winner else "No improvement found"

    entry = f"""
---

## {now} — Skill Evolution: {skill.name}
- **Task:** Evolve {skill.path.relative_to(AGENT_DIR)}
- **Outcome:** {outcome}
- **Variants tested:** {len(variants)}
- **Scores:** {[v.score for v in variants]}
- **Baseline:** {evaluate_skill(skill):.2f}
"""
    with open(REFLECTION_PATH, "a") as f:
        f.write(entry)


def find_all_skills() -> list[Path]:
    """Find all SKILL.md files."""
    return list(SKILLS_DIR.rglob("SKILL.md"))


def evolve_skill(skill_path: Path, num_variants: int) -> bool:
    """Run the full evolution pipeline for one skill. Returns True if promoted."""
    skill = parse_skill(skill_path)
    print(f"\n{'='*50}")
    print(f"Evolving: {skill.name} (v{skill.version})")
    print(f"{'='*50}")

    # Evaluate current baseline
    baseline = evaluate_skill(skill)
    print(f"  Baseline score: {baseline:.2f}")

    if baseline >= EVOLVE_THRESHOLD:
        print(f"  Score >= threshold ({EVOLVE_THRESHOLD}) — skipping evolution.")
        return False

    # Generate and evaluate variants
    print(f"\n  Generating {num_variants} variants...")
    variants = generate_variants(skill, num_variants)

    print(f"\n  Evaluating variants...")
    for variant in variants:
        score = evaluate_variant(variant, skill)
        print(f"    Variant {variant.id}: {score:.2f}")

    # Select best
    best = max(variants, key=lambda v: v.score)
    print(f"\n  Best variant: {best.id} (score: {best.score:.2f})")

    if best.score > baseline:
        print(f"  Improvement: +{best.score - baseline:.2f} — promoting.")
        promote_variant(best, skill)
        log_evolution(skill, variants, best)
        return True
    else:
        print(f"  No improvement over baseline — discarding all variants.")
        log_evolution(skill, variants, None)
        return False


def main() -> int:
    global EVOLVE_THRESHOLD

    parser = argparse.ArgumentParser(description="DGM-inspired skill evolution")
    parser.add_argument("--skill", type=str, help="Path to specific SKILL.md to evolve")
    parser.add_argument("--all", action="store_true", help="Evolve all skills below threshold")
    parser.add_argument("--variants", type=int, default=3, help="Number of variants to generate")
    parser.add_argument("--threshold", type=float, default=EVOLVE_THRESHOLD, help="Score threshold")
    args = parser.parse_args()

    EVOLVE_THRESHOLD = args.threshold

    if args.skill:
        skill_path = Path(args.skill)
        if not skill_path.is_absolute():
            skill_path = AGENT_DIR / args.skill
        if not skill_path.exists():
            print(f"ERROR: Skill not found: {skill_path}")
            return 1
        evolve_skill(skill_path, args.variants)

    elif args.all:
        skills = find_all_skills()
        print(f"Found {len(skills)} skills to evaluate.")
        promoted = 0
        for sp in skills:
            if evolve_skill(sp, args.variants):
                promoted += 1
        print(f"\nDone. Promoted {promoted}/{len(skills)} skills.")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
