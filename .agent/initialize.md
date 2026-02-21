You are an AI agent initializer using the `.agent` blueprint. **Goal:** Configure the `.agent/` folder for a brand-new project so every file reflects the project's actual stack, modules, and conventions.

## Inputs
- Root `README.md`, dependency files (`package.json`, `requirements.txt`, `go.mod`, etc.), directory tree, `git log --oneline -20`.

## Procedure
1. **Scan & Infer:** Read root README, dependency manifests, and directory listing. Infer: project name, language(s), framework(s), database, infra, key modules, build/test/lint commands.
2. **Tailor `.agent/README.md`:** Replace placeholder overview, tech stack table, dependency diagram, and quick commands with inferred values.
3. **Tailor `system/`:** Populate `architecture.md` with inferred components and data flows. Fill `database-schema.md` if ORM/migrations found. Fill `api-endpoints.md` if routes found.
4. **Add project-specific skills:** If React → add `skills/frontend/component-testing/SKILL.md`. If Python → ensure `skills/testing/pytest-patterns/SKILL.md`. Match stack to useful skills.
5. **Add project-specific workflows:** If Docker → add `workflows/deploy.md` with `docker compose` steps. If CI config found → mirror in `workflows/build.md`.
6. **Initialize learning:** Ensure `learning/memory.json` exists (empty entries array). Ensure `learning/reflection-log.md` has a dated starter entry.
7. **Set up automation:** Run `chmod +x automation/*.sh automation/*.py`. If `.git/` exists, symlink `automation/git-hooks/post-commit` → `.git/hooks/post-commit`.
8. **Validate:** List all files created/modified. Confirm no placeholder `TODO` remains in critical paths.
9. **Output:** Emit shell commands to create/update files, then file contents. No explanatory prose.

## Project Details
<!-- Paste project context below, e.g.: "Python FastAPI backend, React frontend, PostgreSQL, deployed on Fly.io" -->
[YOUR PROJECT DETAILS HERE]