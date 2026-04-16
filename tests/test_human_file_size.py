import unittest
from streamonitor.utils.human_file_size import human_file_size

class TestHumanFileSize(unittest.TestCase):

    def test_human_file_size_non_si(self):
        """Test human_file_size with SI=False (Base 1024)"""
        # Testing specific unit boundaries and scaling behavior
        self.assertEqual(human_file_size(0), '0 B')
        self.assertEqual(human_file_size(512), '512 B')
        self.assertEqual(human_file_size(1024), '1 KiB')
        self.assertEqual(human_file_size(1024 * 1024), '1 MiB')
        self.assertEqual(human_file_size(1024 * 1024 * 1024), '1 GiB')
        self.assertEqual(human_file_size(1024 * 1.5), '1.5 KiB')

    def test_human_file_size_si(self):
        """Test human_file_size with SI=True (Base 1000)"""
        # Testing specific unit boundaries and scaling behavior
        self.assertEqual(human_file_size(0, si=True), '0 B')
        self.assertEqual(human_file_size(500, si=True), '500 B')
        self.assertEqual(human_file_size(1000, si=True), '1 KB')
        self.assertEqual(human_file_size(1000 * 1000, si=True), '1 MB')
        self.assertEqual(human_file_size(1000 * 1000 * 1000, si=True), '1 GB')
        self.assertEqual(human_file_size(1500, si=True), '1.5 KB')

    def test_human_file_size_custom_suffix_and_space(self):
        self.assertEqual(human_file_size(1024, suffix='bytes', space='-'), '1-Kibytes')

    def test_human_file_size_fix_decimals(self):
        self.assertEqual(human_file_size(1500, si=True, fix_decimals=2), '1.50 KB')

    def test_human_file_size_negative(self):
        self.assertEqual(human_file_size(-1024), '1 KiB')

    def test_human_file_size_large(self):
        self.assertEqual(human_file_size(1024**4), '1 TiB')
        # The list of units ends at Z or Zi, so larger values than Zi will just be represented with larger numbers in Zi
        self.assertEqual(human_file_size(1024**8), '1024 ZiB')

if __name__ == '__main__':
    unittest.main()
