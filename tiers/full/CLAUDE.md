# CLAUDE.md

Project: [one-line description — what this repo does and why it exists].

> **Always read overarching developer preferences from
> `~/.claude/memory/preferences.md` before generating code.**

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
  - [GLOSSARY.md](GLOSSARY.md) — domain glossary (canonical terms)
  - [docs/adr/](docs/adr/) — decisions with real alternatives considered
    and rejected
  - See [docs/regression-testing-standard.md](https://github.com/benjamininja/project-memory-template/blob/main/docs/regression-testing-standard.md)
    in the template repo before adding tests to a project with real data
    pipelines or multiple runtime surfaces
- **`~/.claude/memory/` (global, cross-project)**:
  - `preferences.md` — working style, cross-project conventions
  - `MEMORY.md` — index across all projects

Read the relevant `.claude/memory/*.md` file before touching project state
that's not obvious from the code alone.

## Project-wide rules

- [Rule 1 — e.g. language/framework conventions, file layout]
- [Rule 2]
- [Rule 3]

## Execution loop

Long agentic builds: plan, execute in stages, and compact at a natural
seam well before the context window fills. `PLAN.md` is the heartbeat,
updated at every seam; `GLOSSARY.md`/`docs/adr/`/`MEMORY.md` crystallize on
real signal, not every step.

---

_This is the **full** tier of `project-memory-template` — the complete
scaffold. See [docs/graduating-tiers.md](https://github.com/benjamininja/project-memory-template/blob/main/docs/graduating-tiers.md) in
the template repo for the reasoning behind each file._
