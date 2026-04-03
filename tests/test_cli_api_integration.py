import os
import sys
import tempfile
import time
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

# Keep imports resilient in minimal test environments.
if "jwt" not in sys.modules:
    sys.modules["jwt"] = types.ModuleType("jwt")

if "filedialpy" not in sys.modules:
    filedialpy = types.ModuleType("filedialpy")
    filedialpy.openFile = lambda **kwargs: None
    sys.modules["filedialpy"] = filedialpy

from reliafy.reliafy import app

# Run as follows to execute API integration tests (skipped by default):
# RELIAFY_RUN_API_TESTS=1 python -m unittest tests.test_cli_api_integration -v

RUN_API_TESTS = os.getenv("RELIAFY_RUN_API_TESTS", "0") == "1"
# API rate limit is 10 req/min; wait this many seconds between requests.
_API_RATE_LIMIT_DELAY = 7
REPO_ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_DIR = REPO_ROOT / "problems"


def _xlsx_contains_text(xlsx_path: Path, text: str) -> bool:
    needle = text.lower().encode("utf-8")
    with zipfile.ZipFile(xlsx_path, "r") as archive:
        for name in archive.namelist():
            if not name.endswith(".xml"):
                continue
            content = archive.read(name).lower()
            if needle in content:
                return True
    return False


@unittest.skipUnless(
    RUN_API_TESTS,
    "API integration tests are disabled. Set RELIAFY_RUN_API_TESTS=1 to run.",
)
class TestCliApiIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def _invoke_with_isolated_results(self, args: list[str]) -> tuple:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)

        results_root = Path(temp_dir.name) / "results"
        results_root.mkdir(parents=True, exist_ok=True)

        with patch("reliafy.utils.api_utils.get_results_dir", return_value=results_root):
            result = self.runner.invoke(app, args)

        return result, results_root

    def _assert_result_artifacts(self, results_root: Path, expect_plot_files: bool):
        json_files = list(results_root.rglob("*.json"))
        xlsx_files = list(results_root.rglob("*.xlsx"))
        pdf_files = list(results_root.rglob("*.pdf"))
        pickle_files = list(results_root.rglob("*.pickle"))

        self.assertTrue(json_files, "Expected at least one JSON result file")
        self.assertTrue(xlsx_files, "Expected at least one Excel result file")

        for path in json_files + xlsx_files:
            self.assertGreater(path.stat().st_size, 0, f"Expected non-empty file: {path}")

        if expect_plot_files:
            self.assertTrue(pdf_files, "Expected at least one PDF result file")
            self.assertTrue(pickle_files, "Expected at least one pickle result file")
            for path in pdf_files + pickle_files:
                self.assertGreater(path.stat().st_size, 0, f"Expected non-empty file: {path}")

        notes_found = any(_xlsx_contains_text(path, "Notes") for path in xlsx_files)
        self.assertTrue(notes_found, "Expected at least one Excel file to contain 'Notes'")

    def test_analyze_examples(self):
        examples = [
            (["analyze", "default", "--problem-file", str(PROBLEMS_DIR / "AT610Problem.py")], True),
            (
                [
                    "analyze",
                    "default",
                    "--include-sorm",
                    "--include-mc",
                    "--problem-file",
                    str(PROBLEMS_DIR / "Chan3Problem.py"),
                ],
                True,
            ),
        ]

        for args, expect_plot_files in examples:
            with self.subTest(command=" ".join(args)):
                result, results_root = self._invoke_with_isolated_results(args)
                self.assertEqual(result.exit_code, 0, msg=result.output)
                self._assert_result_artifacts(results_root, expect_plot_files=expect_plot_files)
            time.sleep(_API_RATE_LIMIT_DELAY)

    def test_design_examples(self):
        examples = [
            ["design", "default", "--problem-file", str(PROBLEMS_DIR / "AT625Problem.py")],
            ["design", "default", "--problem-file", str(PROBLEMS_DIR / "AT624Problem.py")],
            ["design", "default", "--problem-file", str(PROBLEMS_DIR / "Sorensen81Problem.py")],
        ]

        for args in examples:
            with self.subTest(command=" ".join(args)):
                result, results_root = self._invoke_with_isolated_results(args)
                self.assertEqual(result.exit_code, 0, msg=result.output)
                # Design runs typically do not generate plot artifacts.
                self._assert_result_artifacts(results_root, expect_plot_files=False)
            time.sleep(_API_RATE_LIMIT_DELAY)

    def test_simulate_examples(self):
        examples = [
            (["simulate", "default", "--problem-file", str(PROBLEMS_DIR / "Chan2Problem.py")], True),
            (
                [
                    "simulate",
                    "default",
                    "--mc-with-is",
                    "--problem-file",
                    str(PROBLEMS_DIR / "AU2Problem.py"),
                ],
                True,
            ),
        ]

        for args, expect_plot_files in examples:
            with self.subTest(command=" ".join(args)):
                result, results_root = self._invoke_with_isolated_results(args)
                self.assertEqual(result.exit_code, 0, msg=result.output)
                self._assert_result_artifacts(results_root, expect_plot_files=expect_plot_files)
            time.sleep(_API_RATE_LIMIT_DELAY)


if __name__ == "__main__":
    unittest.main()
