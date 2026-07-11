# check-in-hygiene

A [`pre-commit`](https://pre-commit.com) framework hook that scans this
template's memory scaffold at commit time — the "check-in hygiene hook"
noted as future work in this repo's root README Roadmap. Unlike the two
hooks in `skills-plugins-hooks/hooks/` (Claude-Code-native `settings.json`
hooks), this is a `pre-commit` hook deliberately: it needs to catch **every**
commit regardless of tool (terminal, IDE, Claude Code), not just ones Claude
Code itself drives — the same reasoning `skills-plugins-hooks`' ADR-0004
already used for CI over a Claude-Code-only gate applies here.

## What it blocks

1. **Unfilled placeholders** — a staged (added/modified) `CLAUDE.md`,
   `PLAN.md`, `CONTEXT.md`, `.claude/memory/MEMORY.md`, or `docs/adr/*.md`
   (except `0000-adr-template.md` itself, the copy source) that still
   contains bracket-style template text (`[Term]`, `[date]`, etc.) not
   forming a markdown link.
2. **Dangling references** — `CLAUDE.md` or `README.md` linking
   (`[text](path)`) to a relative path that doesn't exist on disk. Checked
   whenever those two files change, **or** whenever a scaffold file is
   deleted/renamed in the same commit — so deleting `CONTEXT.md` without
   touching `CLAUDE.md` still gets caught, since `CLAUDE.md`'s reference to
   it just went stale.

Both checks are scoped to what the **current commit** actually touches —
a pre-existing stale file you aren't editing never blocks an unrelated
commit. This intentionally does **not** attempt git-recency-based
staleness detection ("hasn't been meaningfully updated in N commits") —
that's fuzzy enough to produce false positives, which is exactly the kind
of untrustworthy scaffolding `docs/graduating-tiers.md` already warns
against. Deferred, not forgotten.

There's no interactive "offer to delete" prompt in this first pass —
`pre-commit` hooks need to behave the same at the terminal and in CI, so
this blocks with a clear message and lets you decide (fill in or delete)
yourself.

## Adopt in a consuming repo

Add to that repo's own `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/benjamininja/project-memory-template
    rev: <tag-or-commit-sha>
    hooks:
      - id: check-in-hygiene
```

Requires `pre-commit` (`pip install pre-commit`, then `pre-commit install`
in the consuming repo) — the first real tooling dependency this template
has ever required, versus its previous copy-and-edit-markdown-only nature.
The hook itself is pure Python stdlib (`re`, `pathlib`, `subprocess`) — no
extra Python packages, no `jq`/`sqlite3`-style binary dependency.

It's a no-op (and doesn't even run) on any commit that doesn't touch one of
the scaffold files above, so it costs nothing on ordinary code commits.

## Verify

From a repo with the scaffold copied in:

```bash
cp docs/adr/0000-adr-template.md docs/adr/0001-test.md
git add docs/adr/0001-test.md
python hooks/check-in-hygiene/check_in_hygiene.py
# exit 1, lists the unfilled placeholders

git reset docs/adr/0001-test.md && rm docs/adr/0001-test.md
```
