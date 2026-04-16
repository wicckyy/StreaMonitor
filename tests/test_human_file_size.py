import unittest
import importlib.util
import os

# Dynamically load the module to avoid missing external dependencies in __init__.py files
module_name = "streamonitor_utils_human_file_size"
file_path = os.path.join(os.path.dirname(__file__), "..", "streamonitor", "utils", "human_file_size.py")
spec = importlib.util.spec_from_file_location(module_name, file_path)
human_file_size_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(human_file_size_module)
human_file_size = human_file_size_module.human_file_size


class TestHumanFileSize(unittest.TestCase):
    def test_zero_size(self):
        """Test human_file_size with a size of 0."""
        # Default behavior (binary)
        self.assertEqual(human_file_size(0), "0 B")
        # SI behavior (decimal)
        self.assertEqual(human_file_size(0, si=True), "0 B")
        # Custom space
        self.assertEqual(human_file_size(0, space=""), "0B")
        # Custom suffix
        self.assertEqual(human_file_size(0, suffix="bytes"), "0 bytes")
        # Fixed decimals
        self.assertEqual(human_file_size(0, fix_decimals=2), "0.00 B")

    def test_typical_sizes_binary(self):
        """Test human_file_size with typical sizes using binary units (base 1024)."""
        self.assertEqual(human_file_size(1023), "1023 B")
        self.assertEqual(human_file_size(1024), "1 KiB")
        self.assertEqual(human_file_size(1048576), "1 MiB")
        self.assertEqual(human_file_size(1073741824), "1 GiB")

    def test_typical_sizes_si(self):
        """Test human_file_size with typical sizes using SI units (base 1000)."""
        self.assertEqual(human_file_size(1000, si=True), "1 KB")
        self.assertEqual(human_file_size(1000000, si=True), "1 MB")
        self.assertEqual(human_file_size(1000000000, si=True), "1 GB")

    def test_negative_sizes(self):
        """Test human_file_size with negative sizes (it takes absolute value)."""
        self.assertEqual(human_file_size(-1024), "1 KiB")

    def test_fixed_decimals(self):
        """Test human_file_size with fixed decimals."""
        self.assertEqual(human_file_size(1024, fix_decimals=2), "1.00 KiB")
        self.assertEqual(human_file_size(1536, fix_decimals=1), "1.5 KiB")


if __name__ == "__main__":
    unittest.main()
