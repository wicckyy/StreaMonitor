import unittest
import os
from unittest.mock import MagicMock
from streamonitor.models.video_data import VideoData

class TestVideoData(unittest.TestCase):

    def _create_mock_file(self, filename: str, path: str, size: int) -> MagicMock:
        mock_file = MagicMock(spec=os.DirEntry)
        mock_file.name = filename
        mock_file.path = path
        mock_file.stat.return_value.st_size = size
        return mock_file

    def test_mimetype_mkv_override(self):
        """Test that .mkv files correctly map to video/mp4 for browser compatibility."""
        mock_file = self._create_mock_file('video.mkv', '/tmp/video.mkv', 1024)
        video_data = VideoData(mock_file, 'testuser')
        self.assertEqual(video_data.mimetype, 'video/mp4')

    def test_mimetype_mp4_standard(self):
        """Test that .mp4 files map to video/mp4 as standard."""
        mock_file = self._create_mock_file('video.mp4', '/tmp/video.mp4', 1024)
        video_data = VideoData(mock_file, 'testuser')
        self.assertEqual(video_data.mimetype, 'video/mp4')

    def test_mimetype_unknown(self):
        """Test that unknown extensions fallback appropriately."""
        mock_file = self._create_mock_file('video.unknown', '/tmp/video.unknown', 1024)
        video_data = VideoData(mock_file, 'testuser')
        self.assertEqual(video_data.mimetype, None)
