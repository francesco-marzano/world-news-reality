#!/usr/bin/env python3
"""SessionStart hook: put the current step and the git state in front of the agent."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

MAX_TASKS_CHARS = 4000


def main() -> int:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))
    tasks = root / "TASKS.md"
    if tasks.is_file():
        print("Current TASKS.md:\n" + tasks.read_text(encoding="utf-8")[:MAX_TASKS_CHARS])
    try:
        status = subprocess.run(  # noqa: S603
            ["git", "status", "--short", "--branch"],  # noqa: S607
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 0
    if status.returncode == 0:
        print("git status:\n" + status.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
