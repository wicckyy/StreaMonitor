import unittest
from unittest.mock import patch, MagicMock
from streamonitor.models.video_data import VideoData

class TestVideoData(unittest.TestCase):
    @patch('streamonitor.models.video_data.logger')
    @patch('streamonitor.models.video_data.mimetypes.guess_type')
    def test_mimetype_exception_path(self, mock_guess_type, mock_logger):
        # Mock guess_type to raise an Exception
        test_exception = Exception("Test exception")
        mock_guess_type.side_effect = test_exception

        # We need to mock os.DirEntry
        mock_file = MagicMock()
        mock_file.name = "test_user-20230101-12345.mp4"
        mock_file.path = "/fake/path/test_user-20230101-12345.mp4"

        mock_stat = MagicMock()
        mock_stat.st_size = 1000
        mock_file.stat.return_value = mock_stat

        with patch('streamonitor.utils.human_file_size.human_file_size', return_value='1 KB'):
            # Initialize VideoData
            video_data = VideoData(mock_file, "test_user")

            # Access mimetype property
            mimetype = video_data.mimetype

            # Assert logger.error was called with the exception
            mock_logger.error.assert_called_once_with(test_exception)

            # Assert mimetype returns the default value
            self.assertEqual(mimetype, 'application/octet-stream')

if __name__ == '__main__':
    unittest.main()
