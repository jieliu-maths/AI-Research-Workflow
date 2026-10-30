#!/usr/bin/env python3
"""Check a source tree for common publication leaks; not a complete secret audit."""

import argparse
from pathlib import Path
import re


SKIP = {".git", "__pycache__", ".venv", ".research-workflow", "node_modules"}
TEXT = {".md", ".py", ".json", ".html", ".yaml", ".yml", ".toml", ".txt", ".sh"}
PATTERNS = [
    ("personal home-directory path", re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/")),
    ("Windows home-directory path", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
]


def check(root: Path) -> list[str]:
    problems = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in SKIP for part in relative.parts) or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            problems.append(f"{relative}: symbolic link is not a portable release asset")
            continue
        if not path.is_file():
            continue
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            problems.append(f"{relative}: environment file must not be published")
        if path.suffix in TEXT or path.name in {"workflow", "LICENSE"}:
            text = path.read_text(encoding="utf-8")
            for label, pattern in PATTERNS:
                if pattern.search(text):
                    problems.append(f"{relative}: {label}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    problems = check(args.root)
    for problem in problems:
        print(f"[ERROR] {problem}")
    if not problems:
        print("publication-check: no common path, token, key, or environment-file leaks detected")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
