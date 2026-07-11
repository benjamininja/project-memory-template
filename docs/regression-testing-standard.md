# Regression-testing standard

A complexity-scaled pattern for catching regressions in a project with real
data pipelines and/or multiple runtime surfaces (a notebook/ETL layer, a bot,
a future web frontend) — synthesized from `Python-PowerBI-
DynastyFantasyFootball`'s retrofit, generalized so it isn't Python-specific.

## Principles

1. **Extract pure functions, then unit-test them.** Name-cleaning, hashing,
   parsing, folding — anything with no I/O — belongs in a shared helpers
   module (not copy-pasted per pipeline step) specifically so it *can* be
   unit-tested in isolation. If a function reads a file, hits a network, or
   depends on ambient state, it's not a first-pass unit-test candidate; wrap
   it later as an integration test once the pure core is covered.

2. **Headless-execution tests as pipeline-level checks.** A hand-rolled
   smoke script that exercises real local data (not mocks) and asserts on
   real invariants (schema shape, size limits, business rules) catches
   drift a unit test can't — but only if it runs through a standard
   discoverable runner, not as a one-off script nobody remembers to invoke.
   Converting an existing ad hoc script to the test framework's discovery
   convention (e.g. pytest's `test_*.py` / `test_*()`) costs little and
   turns "a script that exists" into "a check that runs."

3. **Manifest/schema-validation scripts as their own pattern.** A
   machine-checked manifest (e.g. "every external data source is registered
   and its consuming code still exists") is not a unit test and not a
   pipeline smoke test — it's a structural check over the repo's own
   metadata. It's usually already been built as a standalone script by the
   time regression testing is formalized; the win here is wiring the
   already-existing `validate` mode into the fast local gate (pre-commit),
   not rebuilding it.

4. **`pre-commit` as the multi-language orchestrator, chosen up front.**
   Even in a Python-only repo today, pick `pre-commit` (not a Python-only
   runner like `tox`/`nox`) as the local gate's orchestrator *because* it's
   language-agnostic. A future non-Python surface (a web/`vitest`/
   `playwright` frontend, a Node-based tool) adds its own entry to
   `.pre-commit-config.yaml` without requiring the Python layout,
   `pyproject.toml`, or any existing venv split to change. This is a design
   principle, not an implementation detail — state it explicitly wherever
   the standard is adopted, so a future reader doesn't have to re-derive
   why `pre-commit` was chosen over a same-language-only alternative.

5. **Respect existing environment splits.** A repo may deliberately run
   different components in different environments (separate venvs, a
   separate `node_modules`, a separate container) for isolation reasons —
   test tooling must scope to those splits (e.g. per-venv `pyproject.toml`
   `testpaths`), not force a merge for the sake of "one test command."

6. **Visual regression is a later, optional layer.** For projects with a
   dashboard/report surface (Power BI, a web frontend), screenshot-diffing
   is real but meaningfully heavier infrastructure than the layers above.
   Treat it as future work, not part of a first regression-testing pass.

## Minimal example layout

```
pyproject.toml               # [tool.pytest.ini_options], scoped to this env's tests/
tests/
  test_<pure_helpers>.py     # unit tests for extracted pure functions
.pre-commit-config.yaml      # wires a fast structural/manifest check, NOT the full suite
docs/adr/000N-regression-testing-standard.md   # the decision + alternatives, per project convention
```

If a second runtime environment exists (its own venv/toolchain), it gets its
own `tests/` + its own invocation command — don't merge the two into one
runner just to have a single command. A thin wrapper script becomes worth
building only once a third environment or suite shows up (YAGNI).

## What pre-commit runs — and what it deliberately doesn't

`pre-commit` stays local, fast, and advisory: wire in the manifest/schema
validation (principle 3) because it's cheap and catches real drift on every
commit. Do **not** run the full test suite in pre-commit — it's slow, and a
local hook is the wrong enforcement point for "tests must pass before
merge" (see Roadmap below).

## Roadmap — deferred by design, not by neglect

- **CI (e.g. GitHub Actions)** is the architecturally correct place to gate
  merges on the full test suite passing. A local pre-commit/pre-PR hook
  only catches commits made through the tool that installed it — it can't
  catch a PR opened from a different machine, from the GitHub UI, or a
  commit pushed after the PR opens. Adding CI is real, separate work
  (workflow file, runner environment, secrets if any) — log it explicitly
  as future work rather than treating the local hook as a substitute.
- **Visual/screenshot regression** for dashboard or web surfaces — a
  meaningfully heavier lift (screenshot capture + diffing infrastructure)
  than anything above; a seed idea, not a built mechanism, until a project
  actually needs it.
- **Lint/format enforcement** in pre-commit is a separate decision (rule
  selection, auto-fix vs. warn-only, how much existing code suddenly
  flags) — don't bundle it into adopting this standard; it deserves its
  own pass.
