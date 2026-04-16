import unittest
import importlib.util
import os

spec = importlib.util.spec_from_file_location("human_file_size", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "streamonitor", "utils", "human_file_size.py")))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
human_file_size = module.human_file_size

class TestHumanFileSize(unittest.TestCase):
    def test_base_1024(self):
        self.assertEqual(human_file_size(1024), "1 KiB")
        self.assertEqual(human_file_size(1024**2), "1 MiB")
        self.assertEqual(human_file_size(1024**3), "1 GiB")
        self.assertEqual(human_file_size(1500), "1.46 KiB")

    def test_base_1000(self):
        self.assertEqual(human_file_size(1000, si=True), "1 KB")
        self.assertEqual(human_file_size(1000**2, si=True), "1 MB")
        self.assertEqual(human_file_size(1000**3, si=True), "1 GB")
        self.assertEqual(human_file_size(1500, si=True), "1.5 KB")

    def test_edge_cases(self):
        self.assertEqual(human_file_size(0), "0 B")
        self.assertEqual(human_file_size(-1024), "1 KiB") # abs() is used
        # Test max clamping
        self.assertEqual(human_file_size(1024**8), "1024 ZiB") # 1 Yobibyte, limits at ZiB
        self.assertEqual(human_file_size(1000**8, si=True), "1000 ZB")

    def test_formatting_options(self):
        self.assertEqual(human_file_size(1000, fix_decimals=2), "1000.00 B")
        self.assertEqual(human_file_size(1024, fix_decimals=3), "1.000 KiB")
        self.assertEqual(human_file_size(1000, suffix="Bytes"), "1000 Bytes")
        self.assertEqual(human_file_size(1000, space=""), "1000B")
        self.assertEqual(human_file_size(1024, space="-", suffix="b"), "1-Kib")

if __name__ == '__main__':
    unittest.main()
