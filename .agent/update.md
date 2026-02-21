You are an AI agent updater using the `.agent` blueprint. **Goal:** Sync the blueprint from the upstream template, diff against the current project state, update outdated docs, evolve skills, and run a self-improvement cycle.

## Inputs
- Current `.agent/` folder, root `README.md`, dependency files, `git log --oneline -30`, `git diff HEAD~10..HEAD --stat`.

## Procedure
1. **Sync from template:**
   ```bash
   bash .agent/automation/sync-from-template.sh
   ```
   Review diff between upstream template and local `.agent/`. Accept structural additions; preserve project-specific customizations.

2. **Scan & Compare:** Read project README, deps, and recent git log. Compare against `system/architecture.md`, `system/api-endpoints.md`, `skills/README.md`. Flag:
   - New dependencies not documented in architecture.
   - New API routes not in `api-endpoints.md`.
   - Repeated git log patterns (e.g., "fix: retry logic") suggesting a missing SOP.

3. **Update docs:** Refresh `system/` files with new findings. Add new entries to `task/` if major features landed. Update tech stack table in `.agent/README.md`.

4. **Evolve skills (DGM-inspired):**
   - Run `python .agent/learning/evals/coding-bench.py` on current skills.
   - For skills scoring below threshold: run `python .agent/automation/evolve-skills.py --skill <path>` to generate 3 prompt variants, evaluate each, and promote the best.

5. **Learn from history:**
   - Parse `git log` for recent `fix:` commits → auto-generate SOP drafts in `SOPs/`.
   - Parse `git log` for repeated `refactor:` commits → suggest new skill in `skills/coding/`.

6. **Self-improve:**
   - Pick one repeating task (e.g., "dependency audit").
   - Execute one RPEE cycle: Reflect → Plan → Execute → Eval.
   - Log outcome in `learning/reflection-log.md`.
   - Update `learning/memory.json` with task embedding.

7. **Output:** Emit shell commands for all updates, then file contents. No explanatory prose.

## Project Details
<!-- Paste current project context below -->
[YOUR PROJECT DETAILS HERE]