# Model Tips
> Match the model to the task. Each has distinct strengths.

## Claude (Opus / Sonnet)
- **Best for:** Structured reasoning, multi-step planning, long-context analysis, architecture decisions, code review synthesis.
- **Tips:**
  - Use XML tags or markdown headers to structure complex prompts — Claude responds well to explicit structure.
  - For code generation, provide the function signature + docstring + 1-2 examples; Claude infers the rest.
  - Claude excels at "think step by step" prompts for debugging.
  - Use `<artifact>` style output for reusable code blocks.
  - Token budget: Claude handles 100k+ context — use it for repo-wide analysis, but keep *output* requests focused.

## GitHub Copilot
- **Best for:** In-editor line/block completion, boilerplate generation, test scaffolding.
- **Tips:**
  - Write a descriptive function name + docstring → let Copilot complete the body.
  - Open related files in adjacent tabs — Copilot uses open-file context.
  - For test generation: write `def test_` and a descriptive name → Copilot infers the body from the source.
  - Reject and re-trigger (Ctrl+]) if the first suggestion is wrong — subsequent ones are often better.
  - Don't rely on Copilot for cross-file refactors; use a reasoning model instead.

## Codex / Code-Execution Models (o3, o4-mini)
- **Best for:** Deterministic coding tasks, targeted refactors, data transformations, script writing.
- **Tips:**
  - Provide input → expected output examples for data transformation tasks.
  - Use chain-of-thought for complex logic: "First parse X, then map Y, then filter Z."
  - These models are strong at regex, SQL, and shell scripting — lean on them for those.
  - For refactors: provide the before-code and describe the desired change precisely.

## GPT-4.1 / General-Purpose
- **Best for:** Broad tasks, conversational coding, API integration, quick prototyping.
- **Tips:**
  - Good default when you're unsure which model to use.
  - Strong at following complex instruction sets (system prompts).
  - Use function-calling / tool-use format for structured outputs.

## Selection Matrix
| Task Type | Recommended Model | Reason |
|---|---|---|
| Architecture planning | Claude Opus | Deep reasoning, long context |
| Code review | Claude Sonnet | Structured analysis |
| Line-by-line coding | Copilot | Fast, in-editor |
| Refactoring | Codex / o3 | Deterministic transforms |
| Test generation | Copilot + Claude | Copilot for scaffolding, Claude for edge cases |
| Debugging | Claude Opus | Step-by-step reasoning |
| Script writing | Codex / o4-mini | Direct, executable output |
| Documentation | Claude Sonnet | Clear prose, good structure |
