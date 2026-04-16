import unittest
from unittest.mock import MagicMock, patch
import os
from streamonitor.models.video_data import VideoData

class TestVideoData(unittest.TestCase):
    def create_video_data(self, filename, filepath):
        mock_file = MagicMock()
        mock_file.stat.return_value.st_size = 1024
        mock_file.name = filename
        mock_file.path = filepath

        # We patch human_file_size to prevent issues if it uses external missing deps
        with patch('streamonitor.utils.human_file_size.human_file_size', return_value='1 KB'):
            return VideoData(mock_file, "test_user")

    def test_mimetype_mp4(self):
        # Standard behavior
        vd = self.create_video_data("test.mp4", "/path/to/test.mp4")
        self.assertEqual(vd.mimetype, 'video/mp4')

    def test_mimetype_mkv_override(self):
        # MKV override (we lie to Chrome)
        vd = self.create_video_data("test.mkv", "/path/to/test.mkv")
        self.assertEqual(vd.mimetype, 'video/mp4')

    def test_mimetype_unknown_extension(self):
        # Fallback for unknown extension
        vd = self.create_video_data("test.unknown", "/path/to/test.unknown")
        self.assertEqual(vd.mimetype, 'application/octet-stream')

    def test_mimetype_exception_handling(self):
        # Exception during guess_type
        vd = self.create_video_data("test.mp4", "/path/to/test.mp4")
        with patch('mimetypes.guess_type', side_effect=Exception("Test Exception")):
            self.assertEqual(vd.mimetype, 'application/octet-stream')

if __name__ == '__main__':
    unittest.main()
