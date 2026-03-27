import os
import tempfile
import unittest
from pathlib import Path

import yaml

from reliafy.utils.profile_management import save_yaml_profile


class TestProfileFormatting(unittest.TestCase):
    def test_save_yaml_profile_groups_reliability_options(self):
        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                save_yaml_profile("custom", "User-defined profile")

                profile_path = Path(temp_dir) / "profiles" / "custom.yaml"
                profile_text = profile_path.read_text()

                self.assertIn("reliability_options:\n  # FORM\n  form_xtol:", profile_text)
                self.assertIn("\n  # Design\n  design_xtol:", profile_text)
                self.assertIn("\n  # General\n  alpha_direction:", profile_text)
                self.assertIn("\n  # SORM\n  sor_method:", profile_text)
                self.assertIn("\n  # Monte Carlo\n  mc_n:", profile_text)
                self.assertIn("\n  # Importance Sampling\n  is_method:", profile_text)

                loaded_profile = yaml.safe_load(profile_text)
                self.assertIn("reliability_options", loaded_profile)
                self.assertEqual(loaded_profile["name"], "custom")
                self.assertEqual(loaded_profile["description"], "User-defined profile")
            finally:
                os.chdir(previous_cwd)


if __name__ == "__main__":
    unittest.main()
