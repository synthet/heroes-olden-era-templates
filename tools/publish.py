#!/usr/bin/env python3
"""Sync the public template distro from dev onto the main branch worktree."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from paths import PUBLISH_MANIFEST, PUBLISH_WORKTREE, ROOT

MAIN_BRANCH = "main"
DEV_BRANCH = "dev"


def run(args: list[str], *, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=capture,
    )


def load_manifest() -> dict:
    data = json.loads(PUBLISH_MANIFEST.read_text(encoding="utf-8"))
    include = data.get("include", [])
    mapping = data.get("map", {})
    if not include and not mapping:
        raise SystemExit(f"{PUBLISH_MANIFEST} must define include and/or map entries.")
    return data


def ensure_branch() -> None:
    branch = run(["git", "branch", "--show-current"]).stdout.strip()
    if branch != DEV_BRANCH:
        raise SystemExit(f"Run from the {DEV_BRANCH} branch (currently on {branch or 'detached HEAD'}).")


def ensure_worktree() -> Path:
    if PUBLISH_WORKTREE.exists():
        worktree_branch = run(["git", "-C", str(PUBLISH_WORKTREE), "branch", "--show-current"]).stdout.strip()
        if worktree_branch != MAIN_BRANCH:
            raise SystemExit(
                f"{PUBLISH_WORKTREE} exists but is on {worktree_branch!r}, expected {MAIN_BRANCH!r}."
            )
        return PUBLISH_WORKTREE

    run(["git", "worktree", "add", str(PUBLISH_WORKTREE), MAIN_BRANCH], capture=False)
    return PUBLISH_WORKTREE


def sync_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def sync_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def apply_manifest(worktree: Path, manifest: dict) -> None:
    for rel in manifest.get("include", []):
        src = ROOT / rel
        dst = worktree / rel
        if not src.exists():
            raise SystemExit(f"Missing publish source: {src}")
        if src.is_dir():
            sync_tree(src, dst)
        else:
            sync_file(src, dst)

    for src_rel, dst_rel in manifest.get("map", {}).items():
        src = ROOT / src_rel
        dst = worktree / dst_rel
        if not src.exists():
            raise SystemExit(f"Missing publish source: {src}")
        sync_file(src, dst)


def prune_unlisted_paths(worktree: Path, manifest: dict) -> None:
    keep_top = {"templates", "docs", "LICENSE", "README.md"}
    for entry in worktree.iterdir():
        if entry.name == ".git":
            continue
        if entry.name in keep_top:
            continue
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()

    docs_dir = worktree / "docs"
    if docs_dir.is_dir():
        for entry in docs_dir.iterdir():
            if entry.name == "install.md":
                continue
            if entry.is_dir():
                shutil.rmtree(entry)
            else:
                entry.unlink()


def commit_if_dirty(worktree: Path, message: str) -> bool:
    run(["git", "-C", str(worktree), "add", "-A"])
    status = run(["git", "-C", str(worktree), "status", "--porcelain"]).stdout.strip()
    if not status:
        return False
    run(["git", "-C", str(worktree), "commit", "-m", message], capture=False)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish templates/ to the main branch.")
    parser.add_argument(
        "-m",
        "--message",
        default="Update published templates.",
        help="Commit message when the public branch changes.",
    )
    parser.add_argument("--push", action="store_true", help="Push origin/main after committing.")
    parser.add_argument("--dry-run", action="store_true", help="Sync worktree but do not commit or push.")
    args = parser.parse_args()

    ensure_branch()
    manifest = load_manifest()
    worktree = ensure_worktree()
    apply_manifest(worktree, manifest)
    prune_unlisted_paths(worktree, manifest)

    if args.dry_run:
        status = run(["git", "-C", str(worktree), "status", "--short"]).stdout.strip()
        if status:
            print(status)
            print(f"Dry run: changes staged in {worktree}")
        else:
            print("Dry run: public branch already matches dev manifest.")
        return 0

    committed = commit_if_dirty(worktree, args.message)
    if committed:
        print(f"Committed on {MAIN_BRANCH}.")
    else:
        print(f"No changes on {MAIN_BRANCH}.")

    if args.push:
        if committed:
            run(["git", "-C", str(worktree), "push", "origin", MAIN_BRANCH], capture=False)
            print(f"Pushed origin/{MAIN_BRANCH}.")
        else:
            print("Nothing to push.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
