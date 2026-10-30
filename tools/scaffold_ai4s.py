#!/usr/bin/env python3
"""Create a fresh experimental AI4S workspace, with preview and atomic publication."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile


def scaffold(source: Path, target: Path, name: str, apply: bool) -> int:
    target = target.expanduser().absolute()
    # Normalize only the two standard macOS temporary-directory aliases; retain
    # all user-controlled links for the explicit ancestor rejection below.
    if sys.platform == "darwin":
        for alias, canonical in ((Path("/tmp"), Path("/private/tmp")),
                                 (Path("/var"), Path("/private/var"))):
            if alias.is_symlink() and alias.resolve() == canonical and target.is_relative_to(alias):
                target = canonical / target.relative_to(alias)
    if target == Path("/") or target.exists() or target.is_symlink():
        raise ValueError("AI4S requires a new target directory; existing projects are never overwritten")
    if not name.strip():
        raise ValueError("project name must be nonempty")
    for ancestor in (target.parent, *target.parent.parents):
        if ancestor.is_symlink():
            raise ValueError("target ancestors must not be symbolic links")
    if not target.parent.is_dir():
        raise ValueError("create the target parent directory first")
    template = source / "profiles/ai4s/template"
    if not template.is_dir():
        raise ValueError("AI4S template is missing")
    for path in template.rglob("*"):
        if path.is_symlink():
            raise ValueError("AI4S source template must not contain symbolic links")
    assets = [(path, path.relative_to(template)) for path in sorted(template.rglob("*")) if path.is_file()]
    assets += [(source / "tools/evidencectl.py", Path("tools/evidencectl.py")),
               (source / "LICENSE", Path("WORKFLOW-LICENSE"))]
    for path, relative in assets:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"missing or linked source asset: {relative}")
    print(f"profile: ai4s (experimental)\nproject: {name}\ntarget: {target}")
    for _, relative in assets:
        print(f"[CREATE] {relative}")
    if not apply:
        print("preview only; rerun with --apply after reviewing the target")
        return 0
    # Publish a complete fresh scaffold, never partially install into an existing project.
    with tempfile.TemporaryDirectory(prefix=".ai4s-stage-", dir=target.parent) as temporary:
        staged = Path(temporary) / "project"
        staged.mkdir()
        for path, relative in assets:
            destination = staged / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        (staged / "profile.json").write_text(json.dumps({
            "profile": "ai4s", "maturity": "experimental", "project_name": name,
            "canonical_state": "STATE.md", "claims_approved": False,
            "upgrade_support": False,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        # Exclusive directory reservation also refuses a concurrently created target.
        target.mkdir()
        try:
            os.replace(staged, target)
        except BaseException:
            target.rmdir()
            raise
    print("created experimental AI4S scaffold; no hypothesis or research route is approved")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        return scaffold(Path(__file__).resolve().parents[1], args.target,
                        args.project_name or args.target.name, args.apply)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
