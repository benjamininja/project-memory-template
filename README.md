# project-memory-template

A reusable, complexity-scaled project-memory scaffold — `CLAUDE.md` +
`PLAN.md` + `.claude/memory/` + `CONTEXT.md` + `docs/adr/`, sized to how
much a project actually needs, not applied uniformly.

Synthesized from `Python-PowerBI-DynastyFantasyFootball`'s real memory
architecture (built organically over months, growing a piece at a time as
each need showed up) and validated against `skills-plugins-hooks`'
vendored engineering flow (`grill-with-docs`/`domain-modeling`, which
generate `CONTEXT.md`/ADR content live rather than pre-scaffolding it
blank) and ponytail's YAGNI ladder (introduce complexity only as it's
earned).

## Dependency

This template assumes the central skills library,
[`skills-plugins-hooks`](https://github.com/benjamininja/skills-plugins-hooks)
(`ask-matt`, `grill-with-docs`, `domain-modeling`, `tdd`, etc.), is
installed — see that repo's README for the symlink-installation steps.
Every tier's `CLAUDE.md` names this dependency explicitly so a new repo
built from this template doesn't silently assume skills exist without
saying where they come from.

## The three tiers

See [`tiers/`](tiers/) for the actual files, and
[`docs/graduating-tiers.md`](docs/graduating-tiers.md) for exactly when to
add each piece — the additions are **independent triggers**, not a strict
ladder.

- **`tiers/minimal/`** — `CLAUDE.md` + `PLAN.md`. A small script or
  short-lived tool with no real data model or terminology to track.
- **`tiers/standard/`** — adds `.claude/memory/MEMORY.md` (project state
  index) + `CONTEXT.md` (domain glossary). Ongoing state worth remembering,
  but not yet enough decision-density for formal ADRs.
- **`tiers/full/`** — adds `docs/adr/` (numbered decision records) + the
  token-gating execution-loop section in `CLAUDE.md`. Real architectural
  decisions with alternatives worth defending later.

## How to use

Copy the contents of the tier that fits your project into its repo root,
fill in the bracketed placeholders, and delete this note. Start at
`minimal` by default — every project gets `CLAUDE.md`+`PLAN.md` from day
one, since those are living working files with no rot risk. Add
`CONTEXT.md`, `.claude/memory/`, or `docs/adr/` individually, the moment
their specific trigger in `docs/graduating-tiers.md` fires — don't
pre-copy a whole tier bundle "to be safe." An unfilled scaffold file is
worse than no file: it wastes a turn every session it's opened for nothing,
or invites hallucinated content.

No generator script or setup skill ships with this template (deliberately
out of scope for the first pass) — copy-and-edit only.

**Maintaining this template itself:** the three `CLAUDE.md` variants share
an identical preamble (root-preferences pointer, the `skills-plugins-hooks`
dependency note, the `## Git` section) by design — each tier is meant to be
copied independently, so it can't reference a shared include. Nothing
enforces that the three copies stay in sync: if you change the shared
wording in one (e.g. the Git workflow rule), hand-update the other two.

## Roadmap

- ~~**Regression-testing standard**~~ — done, see
  [`docs/regression-testing-standard.md`](docs/regression-testing-standard.md):
  a complexity-scaled pattern (extract-and-unit-test pure functions,
  headless-execution smoke tests via the standard runner, manifest/schema
  validation scripts, `pre-commit` as the language-agnostic orchestrator)
  synthesized from `Python-PowerBI-DynastyFantasyFootball`'s retrofit. CI
  and visual regression are logged as deliberately deferred in the doc's
  own Roadmap section, not built here.
- **Skill distribution beyond manual symlink** — today, using
  `skills-plugins-hooks`' skills in a new repo means manually running its
  README's symlink command. A more portable distribution mechanism
  (bootstrap script, per-repo skill-link manifest) is future work — see the
  matching item in `skills-plugins-hooks/README.md`.
- ~~**Check-in hygiene hook**~~ — done, see
  [`hooks/check-in-hygiene/`](hooks/check-in-hygiene/): a `pre-commit`
  hook blocking commits that leave a copied template placeholder unfilled
  or introduce a dangling `CLAUDE.md`/`README.md` reference. Scoped to
  what the current commit touches, not a full-repo scan — complements, but
  doesn't replace, the per-file graduation triggers above (it can only
  catch problems at commit time, not mid-session). Git-recency-based
  staleness detection and an interactive delete-offer were both considered
  and deliberately deferred — see the hook's own README.
- **Skill-stage/domain routing map** — which vendored skills pair with
  which process stage (Plan / Crystallize / Execute) or domain (e.g.
  `microsoft-docs` for anything Microsoft-related), so a session knows
  what to reach for without re-deriving it. This is a catalog concern owned
  by `skills-plugins-hooks-agents`, not this template — this repo's
  `CLAUDE.md` can reference the map once it exists there.
- ~~**Setup skill**~~ **Done** (2026-07-12) — `setup-project-memory`, in
  `skills-plugins-hooks-agents/skills/`. Scope grew beyond what was
  originally sketched here: instead of just generating
  `CLAUDE.md`/`PLAN.md`/`CONTEXT.md`, it fully bootstraps a new project —
  tier scaffold, `setup-matt-pocock-skills`' config, and `check-in-hygiene`
  pre-commit wiring — in one pass. It lives in the skill-catalog repo, not
  here, since that's the one canonical source every machine
  junction-installs `~/.claude/skills/` from; it reads tier content from
  this repo the same way any consumer would. See that repo's
  [ADR-0005](https://github.com/benjamininja/skills-plugins-hooks-agents/blob/main/docs/adr/0005-skill-routing-and-drift-detection.md)
  for the full reasoning.
