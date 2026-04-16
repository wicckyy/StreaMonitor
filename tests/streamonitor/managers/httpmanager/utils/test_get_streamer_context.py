import unittest
from unittest.mock import Mock, patch
from streamonitor.managers.httpmanager.utils.get_streamer_context import get_streamer_context

class TestGetStreamerContext(unittest.TestCase):
    def setUp(self):
        # mock Bot
        self.bot = Mock()
        self.bot.siteslug = 'test_slug'
        self.bot.video_files_total_size = 300

        # Create some dummy VideoData-like objects
        v1 = Mock()
        v1.filename = 'file_A.mp4'
        v1.filesize = 100

        v2 = Mock()
        v2.filename = 'file_C.mp4'
        v2.filesize = 200

        v3 = Mock()
        v3.filename = 'file_B.mp4'
        v3.filesize = 50

        self.bot.video_files = [v1, v2, v3]
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    @patch('streamonitor.managers.httpmanager.utils.get_streamer_context.confirm_deletes')
    def test_get_streamer_context_sort_by_size(self, mock_confirm_deletes):
        mock_confirm_deletes.return_value = True
        context = get_streamer_context(
            streamer=self.bot,
            sort_by_size=True,
            play_video='file_C.mp4',
            user_agent='test_agent'
        )

        # Check sort by size
        # Should be v2 (200), v1 (100), v3 (50)
        videos = context['videos']
        self.assertEqual(list(videos.keys()), ['file_C.mp4', 'file_A.mp4', 'file_B.mp4'])

        self.assertEqual(context['streamer'], self.bot)
        self.assertEqual(context['video_to_play'], self.v2)
        self.assertEqual(context['total_size'], 300)
        self.assertTrue(context['sort_by_size'])
        self.assertEqual(context['confirm_deletes'], True)
        mock_confirm_deletes.assert_called_once_with('test_agent')

    @patch('streamonitor.managers.httpmanager.utils.get_streamer_context.confirm_deletes')
    def test_get_streamer_context_sort_by_filename(self, mock_confirm_deletes):
        mock_confirm_deletes.return_value = False
        context = get_streamer_context(
            streamer=self.bot,
            sort_by_size=False,
            play_video='file_A.mp4',
            user_agent='other_agent'
        )

        # Check sort by filename (reverse alphabetical)
        # Should be file_C, file_B, file_A
        videos = context['videos']
        self.assertEqual(list(videos.keys()), ['file_C.mp4', 'file_B.mp4', 'file_A.mp4'])

        self.assertEqual(context['video_to_play'], self.v1)
        self.assertFalse(context['sort_by_size'])
        self.assertEqual(context['confirm_deletes'], False)
        mock_confirm_deletes.assert_called_once_with('other_agent')

    @patch('streamonitor.managers.httpmanager.utils.get_streamer_context.confirm_deletes')
    def test_get_streamer_context_play_video_not_found(self, mock_confirm_deletes):
        context = get_streamer_context(
            streamer=self.bot,
            sort_by_size=True,
            play_video='missing.mp4',
            user_agent='test_agent'
        )
        self.assertIsNone(context['video_to_play'])
