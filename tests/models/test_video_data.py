import unittest
from unittest.mock import MagicMock
import os
from streamonitor.models.video_data import VideoData

class TestVideoData(unittest.TestCase):
    def setUp(self):
        self.mock_file = MagicMock(spec=os.DirEntry)
        self.mock_file.path = "/path/to/some/file.mp4"

        # mock stat()
        mock_stat = MagicMock()
        mock_stat.st_size = 1024
        self.mock_file.stat.return_value = mock_stat

    def test_shortname_regex_match(self):
        # Setup mock file to match regex
        self.mock_file.name = "testuser-20231026-123456.mp4"

        # Initialize VideoData
        video_data = VideoData(self.mock_file, "testuser")

        # Verify shortname extracts correctly
        self.assertEqual(video_data.shortname, "20231026-123456")

    def test_shortname_fallback(self):
        # Setup mock file to NOT match regex
        self.mock_file.name = "invalid_format.mp4"

        # Initialize VideoData
        video_data = VideoData(self.mock_file, "testuser")

        # Verify shortname falls back to filename
        self.assertEqual(video_data.shortname, "invalid_format.mp4")

if __name__ == '__main__':
    unittest.main()
