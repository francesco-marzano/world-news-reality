#!/usr/bin/env python3
"""PostToolUse hook: format the file an agent just edited.

Formatting is the formatter's job, so reviews and instructions never spend words on it.
The hook never blocks: on any problem it exits 0 and `just check` reports it later.
"""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
from pathlib import Path

WEB_SUFFIXES = {".ts", ".mjs", ".js", ".json", ".astro", ".css"}


def formatter_command(root: Path, file_path: Path) -> tuple[list[str], Path] | None:
    """Return the command and working directory that format `file_path`, if any."""
    try:
        relative = file_path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    if not relative.parts:
        return None
    top = relative.parts[0]
    if top == "pipeline" and file_path.suffix == ".py":
        return (["uv", "run", "ruff", "format", "--quiet", str(file_path)], root / "pipeline")
    if top == "web" and file_path.suffix in WEB_SUFFIXES:
        return (["pnpm", "exec", "biome", "format", "--write", str(file_path)], root / "web")
    return None


def main() -> int:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))
    command = formatter_command(root, Path(file_path))
    if command is None:
        return 0
    args, cwd = command
    with contextlib.suppress(OSError, subprocess.TimeoutExpired):
        subprocess.run(args, cwd=cwd, capture_output=True, check=False, timeout=60)  # noqa: S603
    return 0


if __name__ == "__main__":
    sys.exit(main())
