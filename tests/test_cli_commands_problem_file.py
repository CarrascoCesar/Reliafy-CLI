import sys
import types
import unittest
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


class _DummyModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def model_dump(self, mode="json"):
        return dict(self.__dict__)


class TestCliProblemFileOption(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.problem_file = Path("problems/AT610Problem.py")

    @staticmethod
    def _build_profile_models():
        run_configuration = _DummyModel()
        reporting_options = _DummyModel()
        rfad_plot_options = _DummyModel()
        # Used by simulate when --plot-lsf is enabled.
        lsf_plot_options = _DummyModel(plot_failure_point=False)
        reliability_options = _DummyModel(is_method="kde")
        return (
            run_configuration,
            reporting_options,
            rfad_plot_options,
            lsf_plot_options,
            reliability_options,
        )

    def test_analyze_passes_problem_file_to_run_app(self):
        models = self._build_profile_models()
        with (
            patch("reliafy.reliafy.ensure_runtime_dirs"),
            patch("reliafy.reliafy.load_profile_models", return_value=models),
            patch("reliafy.reliafy.run_app") as run_app_mock,
        ):
            result = self.runner.invoke(
                app,
                ["analyze", "default", "--problem-file", str(self.problem_file)],
            )

        self.assertEqual(result.exit_code, 0, msg=result.output)
        _, kwargs = run_app_mock.call_args
        self.assertEqual(kwargs.get("problem_file_path"), self.problem_file)

    def test_design_passes_problem_file_to_run_app(self):
        models = self._build_profile_models()
        with (
            patch("reliafy.reliafy.ensure_runtime_dirs"),
            patch("reliafy.reliafy.load_profile_models", return_value=models),
            patch("reliafy.reliafy.run_app") as run_app_mock,
        ):
            result = self.runner.invoke(
                app,
                ["design", "default", "--problem-file", str(self.problem_file)],
            )

        self.assertEqual(result.exit_code, 0, msg=result.output)
        _, kwargs = run_app_mock.call_args
        self.assertEqual(kwargs.get("problem_file_path"), self.problem_file)

    def test_simulate_passes_problem_file_to_run_app(self):
        models = self._build_profile_models()
        with (
            patch("reliafy.reliafy.ensure_runtime_dirs"),
            patch("reliafy.reliafy.load_profile_models", return_value=models),
            patch("reliafy.reliafy.run_app") as run_app_mock,
        ):
            result = self.runner.invoke(
                app,
                ["simulate", "default", "--problem-file", str(self.problem_file)],
            )

        self.assertEqual(result.exit_code, 0, msg=result.output)
        _, kwargs = run_app_mock.call_args
        self.assertEqual(kwargs.get("problem_file_path"), self.problem_file)


if __name__ == "__main__":
    unittest.main()
