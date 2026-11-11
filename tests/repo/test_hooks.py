"""Tests for the agent hooks in .claude/hooks. Standard library only."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from types import ModuleType
from unittest import mock

HOOKS = Path(__file__).resolve().parents[2] / ".claude" / "hooks"


def load_hook(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, HOOKS / f"{name}.py")
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stop_check = load_hook("stop_check")
format_file = load_hook("format_file")


class TaskStatusTest(unittest.TestCase):
    def test_reads_the_status_line(self) -> None:
        self.assertEqual(stop_check.task_status("# TASKS\nStatus: done\n"), "done")

    def test_is_case_insensitive_on_the_value(self) -> None:
        self.assertEqual(stop_check.task_status("Status: In-Progress\n"), "in-progress")

    def test_returns_none_without_a_status_line(self) -> None:
        self.assertIsNone(stop_check.task_status("# TASKS\nThe status: done maybe\n"))


class ShouldRunCheckTest(unittest.TestCase):
    def test_runs_for_a_finished_step(self) -> None:
        self.assertTrue(stop_check.should_run_check({}, "done"))

    def test_never_runs_while_already_continuing_from_the_hook(self) -> None:
        self.assertFalse(stop_check.should_run_check({"stop_hook_active": True}, "done"))

    def test_stays_out_of_the_way_for_other_statuses(self) -> None:
        for status in ("in-progress", "awaiting-approval", "blocked", None):
            with self.subTest(status=status):
                self.assertFalse(stop_check.should_run_check({}, status))


class StopCheckMainTest(unittest.TestCase):
    def run_main(self, root: Path, payload: dict[str, object], check_exit: int) -> tuple[int, str]:
        completed = subprocess.CompletedProcess(["just", "check"], check_exit, "boom\n", "")
        stderr = io.StringIO()
        with (
            mock.patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": str(root)}),
            mock.patch.object(sys, "stdin", io.StringIO(json.dumps(payload))),
            mock.patch.object(stop_check.shutil, "which", return_value="/usr/bin/just"),
            mock.patch.object(stop_check, "tree_fingerprint", return_value="abc"),
            mock.patch.object(stop_check.subprocess, "run", return_value=completed) as run,
            redirect_stderr(stderr),
        ):
            code = stop_check.main()
        self.calls = run.call_count
        return code, stderr.getvalue()

    def test_blocks_with_exit_2_when_the_check_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "TASKS.md").write_text("Status: done\n", encoding="utf-8")

            code, stderr = self.run_main(root, {}, check_exit=1)

            self.assertEqual(code, 2)
            self.assertIn("just check", stderr)
            self.assertIn("boom", stderr)

    def test_passes_and_remembers_a_green_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "TASKS.md").write_text("Status: done\n", encoding="utf-8")

            first, _ = self.run_main(root, {}, check_exit=0)
            calls_first = self.calls
            second, _ = self.run_main(root, {}, check_exit=0)

            self.assertEqual((first, second), (0, 0))
            self.assertEqual(calls_first, 1)
            self.assertEqual(self.calls, 0, "an unchanged tree must not be checked twice")

    def test_does_not_run_the_check_while_work_is_in_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "TASKS.md").write_text("Status: in-progress\n", encoding="utf-8")

            code, _ = self.run_main(root, {}, check_exit=1)

            self.assertEqual(code, 0)
            self.assertEqual(self.calls, 0)

    def test_tolerates_a_missing_tasks_file_and_empty_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _ = self.run_main(Path(tmp), {}, check_exit=1)

            self.assertEqual(code, 0)


class FormatterCommandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path("/repo")

    def test_python_under_pipeline_uses_ruff(self) -> None:
        command = format_file.formatter_command(self.root, self.root / "pipeline/src/a.py")

        self.assertIsNotNone(command)
        args, cwd = command
        self.assertEqual(args[:4], ["uv", "run", "ruff", "format"])
        self.assertEqual(cwd, self.root / "pipeline")

    def test_typescript_under_web_uses_biome(self) -> None:
        command = format_file.formatter_command(self.root, self.root / "web/src/lib/time.ts")

        self.assertIsNotNone(command)
        args, cwd = command
        self.assertEqual(args[:3], ["pnpm", "exec", "biome"])
        self.assertEqual(cwd, self.root / "web")

    def test_other_files_are_left_alone(self) -> None:
        for path in ("README.md", "config/metrics.yaml", "web/README.md", "pipeline/uv.lock"):
            with self.subTest(path=path):
                self.assertIsNone(format_file.formatter_command(self.root, self.root / path))

    def test_files_outside_the_repository_are_left_alone(self) -> None:
        self.assertIsNone(format_file.formatter_command(self.root, Path("/etc/passwd.py")))


if __name__ == "__main__":
    unittest.main()
