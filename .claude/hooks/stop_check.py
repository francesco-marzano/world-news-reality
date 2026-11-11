#!/usr/bin/env python3
"""Stop hook: when TASKS.md says the step is done, `just check` must pass.

The hook stays out of the way in every other case, so an agent can stop freely while
it waits for approval, is blocked, or has failing tests written on purpose:

- status in TASKS.md is not `done`;
- Claude Code is already continuing because of this hook (`stop_hook_active`);
- `just` is not installed;
- the working tree is identical to the last one that passed.

Exit code 2 sends stderr back to the agent as the reason to keep working.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

STATUS_LINE = re.compile(r"^Status:\s*(\S+)\s*$", re.MULTILINE)
TAIL_LINES = 60


def task_status(tasks_text: str) -> str | None:
    """Return the status declared in TASKS.md, or None when there is no status line."""
    match = STATUS_LINE.search(tasks_text)
    return match.group(1).lower() if match else None


def should_run_check(payload: dict[str, object], status: str | None) -> bool:
    """Run the check only for a finished step, and never twice in a row."""
    return status == "done" and not payload.get("stop_hook_active", False)


def tree_fingerprint(root: Path) -> str:
    """Identify the current commit plus every uncommitted change."""
    digest = hashlib.sha256()
    for command in (
        ["git", "rev-parse", "HEAD"],
        ["git", "status", "--porcelain"],
        ["git", "diff", "HEAD"],
    ):
        result = subprocess.run(command, cwd=root, capture_output=True, check=False)  # noqa: S603
        digest.update(result.stdout)
    untracked = subprocess.run(  # noqa: S603
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],  # noqa: S607
        cwd=root,
        capture_output=True,
        check=False,
    )
    for name in sorted(filter(None, untracked.stdout.split(b"\0"))):
        path = root / os.fsdecode(name)
        digest.update(name)
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    raw = sys.stdin.read()
    payload: dict[str, object] = json.loads(raw) if raw.strip() else {}
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))
    tasks = root / "TASKS.md"
    status = task_status(tasks.read_text(encoding="utf-8")) if tasks.is_file() else None

    if not should_run_check(payload, status):
        return 0
    if shutil.which("just") is None:
        print("stop_check: `just` is not installed, skipping the check", file=sys.stderr)
        return 0

    cache = root / ".claude" / ".cache" / "stop_check"
    fingerprint = tree_fingerprint(root)
    if cache.is_file() and cache.read_text(encoding="utf-8") == fingerprint:
        return 0

    result = subprocess.run(  # noqa: S603
        ["just", "check"],  # noqa: S607
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        tail = (result.stdout + result.stderr).splitlines()[-TAIL_LINES:]
        print(
            "TASKS.md says the step is done, but `just check` fails. "
            "Fix it, or set the status back to in-progress or blocked.\n" + "\n".join(tail),
            file=sys.stderr,
        )
        return 2

    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(fingerprint, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
