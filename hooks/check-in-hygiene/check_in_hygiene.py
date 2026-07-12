#!/usr/bin/env python3
"""check-in-hygiene — pre-commit hook for project-memory-template's scaffold.

Blocks a commit when:
  1. A staged (added/modified) scaffold file still contains unfilled
     template placeholder text (`[bracket text]` not immediately followed
     by `(` — i.e. not a markdown link) — 0000-adr-template.md is exempt,
     it's the copy source and is meant to keep its placeholders forever.
  2. CLAUDE.md or README.md reference a relative file path that doesn't
     exist on disk — checked whenever CLAUDE.md/README.md themselves
     change, or whenever a scaffold file is deleted/renamed in this
     commit (so a reference that just went dangling is still caught even
     if the file naming the reference wasn't itself touched).

Reads the staged diff directly via `git diff --cached --name-status`
rather than trusting pre-commit's passed argv (this hook runs with
pass_filenames: false), so deletions are visible regardless of how
pre-commit would otherwise filter them.

Scoped to what THIS commit touches, not a full-repo scan — a pre-existing
stale file you aren't editing never blocks an unrelated commit.

ponytail: the placeholder heuristic (bracket text not forming a markdown
link) will false-negative on a placeholder someone accidentally wrapped in
link syntax. Good enough for a first pass; tighten if it bites in practice.
Markdown task-list checkboxes (`[ ]`/`[x]`/`[X]`) are excluded explicitly —
bit on the very first real commit against a PLAN.md using them.
Brackets directly preceded by a word character or backtick are excluded
too — DAX column/measure references (`Dim_Contract[CapHitPct]`, inline-code
`[CapHit]`) bit on the first Dynasty PLAN.md commit after adoption; real
template placeholders always follow whitespace or punctuation.
"""
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDER_CHECK_FILES = {"CLAUDE.md", "PLAN.md", "CONTEXT.md", ".claude/memory/MEMORY.md"}
ADR_TEMPLATE_NAME = "0000-adr-template.md"
LINK_CHECK_FILES = {"CLAUDE.md", "README.md"}

PLACEHOLDER_RE = re.compile(r"(?<![\w`\]])\[(?![ xX]\])[^\]\n]+\](?!\()")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]+\]\(([^)]+)\)")


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return Path(out)


def staged_changes() -> dict:
    """Return {path: status_letter} for staged files, e.g. {'CONTEXT.md': 'D'}."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-status"],
        capture_output=True, text=True, check=True,
    ).stdout
    changes = {}
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        changes[path] = status[0]  # 'A', 'M', 'D', 'R100' -> 'R'
    return changes


def is_adr_path(path: str) -> bool:
    return (
        path.startswith("docs/adr/")
        and path.endswith(".md")
        and Path(path).name != ADR_TEMPLATE_NAME
    )


def check_placeholders(root: Path, changes: dict) -> list:
    problems = []
    for path, status in changes.items():
        if status == "D":
            continue
        if path not in PLACEHOLDER_CHECK_FILES and not is_adr_path(path):
            continue
        full = root / path
        if not full.exists():
            continue
        text = full.read_text(encoding="utf-8", errors="ignore")
        matches = PLACEHOLDER_RE.findall(text)
        if matches:
            shown = ", ".join(matches[:3])
            more = f" (+{len(matches) - 3} more)" if len(matches) > 3 else ""
            problems.append(f"{path}: unfilled placeholder(s) still present: {shown}{more}")
    return problems


def check_dangling_references(root: Path, changes: dict) -> list:
    problems = []
    deleted_or_renamed = {
        path for path, status in changes.items()
        if status == "D" or status.startswith("R")
    }
    trigger = bool(deleted_or_renamed) or any(path in LINK_CHECK_FILES for path in changes)
    if not trigger:
        return problems

    for name in LINK_CHECK_FILES:
        full = root / name
        if not full.exists():
            continue
        text = full.read_text(encoding="utf-8", errors="ignore")
        for link in MARKDOWN_LINK_RE.findall(text):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = (full.parent / link.split("#")[0]).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                continue  # points outside the repo (e.g. an absolute machine path) — not ours to judge
            if not target.exists():
                problems.append(f"{name}: dangling reference to '{link}' — target does not exist")
    return problems


def main() -> int:
    root = repo_root()
    changes = staged_changes()
    problems = check_placeholders(root, changes) + check_dangling_references(root, changes)
    if problems:
        print("check-in-hygiene: blocked commit —", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "\nFill in the placeholder(s) or delete the file, or fix/remove the dangling "
            "reference, then re-commit.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
