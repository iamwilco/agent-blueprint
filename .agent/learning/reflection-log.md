# Reflection Log
> Agents append here after each non-trivial task. Entries are parsed by `workflows/self-improve.md` to identify recurring patterns and evolution candidates.

---

## 2025-01-15 — Example: CI Pipeline Setup
- **Task:** Set up GitHub Actions CI with build, test, lint stages.
- **Outcome:** Success (score: 0.92)
- **What went well:** Docker layer caching halved build time. Matrix strategy covered Python 3.11 + 3.12.
- **What failed:** Initial YAML indentation error caused 2 failed runs.
- **Root cause:** Copied template without validating syntax.
- **Improvement applied:** Added `actionlint` to pre-commit hooks.
- **Follow-up eval:** CI runs green for 5 consecutive commits.
- **SOP created:** No (too simple).
- **Skill evolved:** No.

---

## 2025-01-16 — Example: Flaky Integration Test Fix
- **Task:** Diagnose and fix flaky test_create_user_cascade in auth module.
- **Outcome:** Success (score: 0.78)
- **What went well:** Identified shared DB state via test isolation analysis.
- **What failed:** First fix attempt (adding sleep) was a band-aid; had to redo.
- **Root cause:** Tests shared a DB connection without transaction rollback.
- **Improvement applied:** Switched to per-test transaction rollback fixture.
- **Follow-up eval:** 50 consecutive green runs on that test.
- **SOP created:** `SOPs/debugging/flaky-test-fix.md`
- **Skill evolved:** Added transaction rollback pattern to `skills/testing/integration-testing/SKILL.md`.

---

## YYYY-MM-DD — Template
- **Task:**
- **Outcome:** success | partial | failure (score: X.XX)
- **What went well:**
- **What failed:**
- **Root cause:**
- **Improvement applied:**
- **Follow-up eval:**
- **SOP created:** path or No
- **Skill evolved:** path or No

---

## 2026-02-21 — Skill Evolution: Refactor Assistant
- **Task:** Evolve skills/coding/refactor-assistant/SKILL.md
- **Outcome:** Promoted variant 0 (0.79)
- **Variants tested:** 3
- **Scores:** [0.788, 0.694, 0.623]
- **Baseline:** 0.70

---

## 2026-02-21 — Skill Evolution: Git Commit Formatter
- **Task:** Evolve skills/coding/git-commit-formatter/SKILL.md
- **Outcome:** Promoted variant 0 (0.78)
- **Variants tested:** 3
- **Scores:** [0.778, 0.631, 0.771]
- **Baseline:** 0.70

---

## 2026-02-21 — Skill Evolution: Docker Build & Deploy
- **Task:** Evolve skills/deployment/docker-build/SKILL.md
- **Outcome:** Promoted variant 2 (0.80)
- **Variants tested:** 3
- **Scores:** [0.605, 0.721, 0.799]
- **Baseline:** 0.70

---

## 2026-02-21 — Skill Evolution: [Domain-Specific Encoding/Decoding]
- **Task:** Evolve skills/blockchain/bech32-encoding-decoding/SKILL.md
- **Outcome:** Promoted variant 1 (0.81)
- **Variants tested:** 3
- **Scores:** [0.63, 0.811, 0.697]
- **Baseline:** 0.70

---

## 2026-02-21 — Skill Evolution: Integration Testing
- **Task:** Evolve skills/testing/integration-testing/SKILL.md
- **Outcome:** Promoted variant 0 (0.80)
- **Variants tested:** 3
- **Scores:** [0.802, 0.671, 0.706]
- **Baseline:** 0.70

---

## 2026-02-21 — Skill Evolution: Unit Testing
- **Task:** Evolve skills/testing/unit-testing/SKILL.md
- **Outcome:** Promoted variant 2 (0.70)
- **Variants tested:** 3
- **Scores:** [0.643, 0.689, 0.701]
- **Baseline:** 0.70
