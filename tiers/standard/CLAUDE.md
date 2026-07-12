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
  - [MEMORY.md](.claude/memory/MEMORY.md) — index of project facts and state
  - [CONTEXT.md](CONTEXT.md) — domain glossary (canonical terms)
- **`C:\Users\benha\.claude\memory\` (global, cross-project)**:
  - `preferences.md` — working style, cross-project conventions
  - `MEMORY.md` — index across all projects

Read the relevant `.claude/memory/*.md` file before touching project state
it's not obvious from the code alone.

## Project-wide rules

- [Rule 1 — e.g. language/framework conventions, file layout]
- [Rule 2]
- [Rule 3]

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

---

_This is the **standard** tier of `project-memory-template` — no
`docs/adr/` yet (decisions log inline in `MEMORY.md`/`PLAN.md`). See
[docs/graduating-tiers.md](../../docs/graduating-tiers.md) in the template
repo for when to add it._
