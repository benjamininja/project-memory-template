# CLAUDE.md

Project: [one-line description — what this repo does and why it exists].

> **Always read overarching developer preferences from
> `C:\Users\benha\.claude\memory\preferences.md` before generating code.**

> Skills used in this project are sourced from the central
> `skills-plugins-hooks-agents` repo (`benjamininja/skills-plugins-hooks-agents`) —
> installed per that repo's README (symlinked into `~/.claude/skills/`).
> If a skill this project needs isn't available, check there first before
> writing one-off logic.

## Memory layout

Two memory stores, different scopes:

- **`.claude/memory/` (this repo, project-specific)**:
  - [MEMORY.md](.claude/memory/MEMORY.md) — index of project facts, state,
    and ADR pointers
  - [CONTEXT.md](CONTEXT.md) — domain glossary (canonical terms)
  - [docs/adr/](docs/adr/) — decisions with real alternatives considered
    and rejected
  - See [docs/regression-testing-standard.md](../../docs/regression-testing-standard.md)
    in the template repo before adding tests to a project with real data
    pipelines or multiple runtime surfaces
- **`C:\Users\benha\.claude\memory\` (global, cross-project)**:
  - `preferences.md` — working style, cross-project conventions
  - `MEMORY.md` — index across all projects

Read the relevant `.claude/memory/*.md` file before touching project state
that's not obvious from the code alone.

## Project-wide rules

- [Rule 1 — e.g. language/framework conventions, file layout]
- [Rule 2]
- [Rule 3]

## Execution loop

Long agentic builds follow the token-gated loop: `grill/plan → (Phase 0
consolidate) → compact → execute stage → compact → …` — compact at a
model-relative budget (~35% on Opus). See root
`token-gating-loop.md`. `PLAN.md` is the heartbeat, updated every seam;
`CONTEXT.md`/`docs/adr/`/`MEMORY.md` crystallize on real signal, not every
step.

## Plan gate

<!-- Invariant mirrored from the root ~/.claude/CLAUDE.md plan gate
     (benjamininja/dotclaude). Threshold/escape-hatch changes update both
     copies and all three tiers. -->

Non-trivial changes — a new file, more than one file touched, any design
decision — follow **plan → explicit confirmation → write**. Enter plan
mode by default for work over that threshold. Only escape hatches: an
explicit "just do it", or typo-class fixes (single line, zero design
content).

## Git

Feature branch → `main` via PR. Never commit or push directly to `main`.
Commit only when asked.

Before opening a PR, run `/security-review` on the diff.

---

_This is the **full** tier of `project-memory-template` — the complete
scaffold. See [docs/graduating-tiers.md](../../docs/graduating-tiers.md) in
the template repo for the reasoning behind each file._
