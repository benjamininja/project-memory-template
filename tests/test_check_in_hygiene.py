"""Regression tests for hooks/check-in-hygiene/check_in_hygiene.py.

Pure-function cases cover the placeholder regex (every false positive that
shipped as a fix is pinned here: #8 checkboxes, #10 DAX brackets). Integration
cases run the hook against a throwaway git repo with real staged changes, the
same way pre-commit invokes it.
"""
import subprocess

import pytest

import check_in_hygiene as hyg

GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.com",
}


# --- pure: placeholder regex -------------------------------------------------

@pytest.mark.parametrize("text", [
    "Project: [one-line description — what this repo does].",
    "- [Rule 1 — e.g. language/framework conventions]",
    "## Working state ([date])",
    "- [ ] [Work item, note what it's blocked on]",
])
def test_placeholder_regex_flags_unfilled_template_text(text):
    assert hyg.PLACEHOLDER_RE.search(text)


@pytest.mark.parametrize("text", [
    "- [ ] open task",          # checkbox, PR #8
    "- [x] done task",
    "- [X] done task",
    "Dim_Contract[CapHitPct]",  # DAX column reference, PR #10
    "use `[CapHit]` here",      # inline-code DAX measure, PR #10
    "see [the docs](docs/a.md)",  # markdown link
    "no brackets at all",
])
def test_placeholder_regex_ignores_legitimate_brackets(text):
    assert not hyg.PLACEHOLDER_RE.search(text)


@pytest.mark.xfail(
    strict=True,
    reason="known gap: [[wikilink]] is flagged as a placeholder; remove xfail once fixed",
)
def test_wikilink_is_not_a_placeholder():
    assert not hyg.PLACEHOLDER_RE.search("see [[memory-architecture]]")


@pytest.mark.parametrize("path,expected", [
    ("docs/adr/0001-decision.md", True),
    ("docs/adr/0000-adr-template.md", False),
    ("docs/adr/notes.txt", False),
    ("other/docs/adr/0001-x.md", False),
])
def test_is_adr_path(path, expected):
    assert hyg.is_adr_path(path) is expected


# --- integration: real staged changes in a temp git repo ---------------------

@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path.resolve()
    monkeypatch.chdir(root)
    for key, value in GIT_ENV.items():
        monkeypatch.setenv(key, value)
    git(root, "init", "-q")
    git(root, "config", "core.autocrlf", "false")
    return root


def git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def stage(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    git(root, "add", rel)


def test_filled_claude_md_passes(repo, capsys):
    stage(repo, "CLAUDE.md", "# CLAUDE.md\n\nProject: a real description.\n")
    assert hyg.main() == 0


def test_unfilled_placeholder_blocks_commit(repo, capsys):
    stage(repo, "CLAUDE.md", "Project: [one-line description].\n")
    assert hyg.main() == 1
    assert "unfilled placeholder" in capsys.readouterr().err


def test_adr_template_is_exempt(repo):
    stage(repo, "docs/adr/0000-adr-template.md", "# [Title]\n\n[Context goes here]\n")
    assert hyg.main() == 0


def test_placeholder_in_unscoped_file_is_ignored(repo):
    stage(repo, "notes.txt", "[todo]\n")
    assert hyg.main() == 0


def test_dangling_link_in_readme_blocks_commit(repo, capsys):
    stage(repo, "README.md", "See [guide](docs/missing.md).\n")
    assert hyg.main() == 1
    assert "dangling reference" in capsys.readouterr().err


def test_valid_link_passes(repo):
    stage(repo, "docs/guide.md", "# guide\n")
    stage(repo, "README.md", "See [guide](docs/guide.md).\n")
    assert hyg.main() == 0


def test_link_pointing_outside_repo_is_not_judged(repo):
    stage(repo, "README.md", "See [elsewhere](../../outside.md).\n")
    assert hyg.main() == 0


def test_remote_and_anchor_links_are_skipped(repo):
    stage(repo, "README.md", "[a](https://example.com) [b](#section) [c](mailto:x@y.z)\n")
    assert hyg.main() == 0


def test_deleting_a_referenced_file_is_caught(repo, capsys):
    stage(repo, "docs/guide.md", "# guide\n")
    stage(repo, "README.md", "See [guide](docs/guide.md).\n")
    git(repo, "commit", "-q", "-m", "init")
    git(repo, "rm", "-q", "docs/guide.md")
    assert hyg.main() == 1
    assert "docs/guide.md" in capsys.readouterr().err


def test_nothing_staged_passes(repo):
    assert hyg.main() == 0
