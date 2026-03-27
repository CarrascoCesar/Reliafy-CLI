import unittest
import importlib

class TestReliafyCliMain(unittest.TestCase):
    def test_main_module_imports(self):
        # Ensure __main__ imports without triggering execution
        mod = importlib.import_module('reliafy.__main__')
        self.assertTrue(hasattr(mod, '__name__'))

    def test_entrypoint_callable(self):
        # Ensure reliafy.main exists and is callable
        from reliafy import main
        self.assertTrue(callable(main))

if __name__ == "__main__":
    unittest.main()
