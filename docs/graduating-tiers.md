# Graduating tiers

The `minimal`/`standard`/`full` labels in [`tiers/`](../tiers/) are
shorthand for "how many of these files you've accumulated," not a gate you
pass through in strict order. The three additions past `minimal` are
**independent triggers** — a project can hit one without the others.

## Add `.claude/memory/` (+ `MEMORY.md`)

**Trigger:** you catch yourself re-deriving the same project fact or state
across sessions — a decision that was already made, a schema detail, a
piece of history that isn't obvious from the code alone.

The trigger is state accumulation, not file count. A one-file `MEMORY.md`
index is enough until you have more than one distinct topic worth its own
file (data model, a subsystem, an external integration) — then split.

**How to split, once it's warranted:** pull each distinct topic into its own
`.claude/memory/<topic>.md` (name it for the topic, not a date or a ticket —
`data-model.md`, not `2026-06-notes.md`), and turn `MEMORY.md` into an index
of one-line pointers to each, not a place where the content itself lives.
`MEMORY.md` keeps a short "Decisions" log inline for as long as that stays
short — once decisions need their own record with alternatives considered,
that's the separate `docs/adr/` trigger below, not another memory-file
split.

## Add `CONTEXT.md`

**Trigger:** you catch yourself re-explaining the same term or convention,
or a name is ambiguous without a definition (does "session" mean the same
thing every time it's used in this codebase?).

Independent of whether you have any ADRs or `.claude/memory/` yet — a
jargon-heavy small tool can need a glossary on day one with no other
memory infrastructure at all.

**How to organize it, once it grows past a handful of terms:** group
related terms under `###` subsections by theme (e.g. "Assets & identity",
"Time", "Teams & divisions" — group by what the terms are *about*, not by
when they were added). A flat, ungrouped list stops being navigable well
before it stops being short.

## Add `docs/adr/`

**Trigger:** the first time you make a decision with real alternatives
considered and rejected, where a future reader would reasonably ask "why
not X instead?" Not every decision — routine ones belong in `PLAN.md`'s
Shipped section as a one-liner. An ADR is for decisions worth defending
later.

Independent of whether `.claude/memory/` or `CONTEXT.md` exist yet — a
single high-stakes infrastructure choice can warrant an ADR in an otherwise
`minimal`-tier project.

## Why not just always ship `full`?

Empty scaffolding rots. Pocock's `grill-with-docs`/`domain-modeling` skills
(vendored in `skills-plugins-hooks-agents`) never pre-create a blank `CONTEXT.md`
or ADR — they generate the file live, at the moment a real term or decision
exists. A `CLAUDE.md` that points at an empty `CONTEXT.md` wastes a turn (or
invites hallucinated content) every session until someone fills it in.
Copy only the files whose trigger has actually fired.
