import unittest
from unittest.mock import Mock
import os
import sys

# Add parent directory to sys.path to allow streamonitor imports if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from streamonitor.models.video_data import VideoData

class TestVideoData(unittest.TestCase):
    def _create_mock_file(self, name):
        mock_file = Mock(spec=os.DirEntry)
        mock_file.name = name
        mock_file.path = f'/mock/path/{name}'
        mock_stat = Mock()
        mock_stat.st_size = 1024
        mock_file.stat.return_value = mock_stat
        return mock_file

    def test_shortname_match(self):
        # Happy path
        mock_file = self._create_mock_file('testuser-20231024-123456.mp4')
        vd = VideoData(mock_file, 'testuser')
        self.assertEqual(vd.shortname, '20231024-123456')

    def test_shortname_no_match(self):
        # No match path
        mock_file = self._create_mock_file('some_other_name.mp4')
        vd = VideoData(mock_file, 'testuser')
        self.assertEqual(vd.shortname, 'some_other_name.mp4')

    def test_shortname_ignore_case(self):
        # Ignore case path
        mock_file = self._create_mock_file('TeStUsEr-20231024-123456.mp4')
        vd = VideoData(mock_file, 'testuser')
        self.assertEqual(vd.shortname, '20231024-123456')

    def test_shortname_missing_trailing_digits(self):
        # Edge case missing the digits after the dash
        mock_file = self._create_mock_file('testuser-20231024-.mp4')
        vd = VideoData(mock_file, 'testuser')
        self.assertEqual(vd.shortname, '20231024-')

if __name__ == '__main__':
    unittest.main()
