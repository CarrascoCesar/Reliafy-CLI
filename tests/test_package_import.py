import unittest

class TestReliafyPackageImport(unittest.TestCase):
    def test_import_and_main_exposed(self):
        import reliafy
        self.assertTrue(hasattr(reliafy, "main"), "reliafy should expose main in __init__")

if __name__ == "__main__":
    unittest.main()
