import unittest
from streamonitor.enums import Status
from unittest.mock import Mock
from streamonitor.managers.httpmanager.filters import status_icon

class TestFilters(unittest.TestCase):

    def test_status_icon_recording(self):
        """Test status_icon when streamer is recording."""
        streamer = Mock()
        streamer.recording = True
        streamer.sc = Status.PUBLIC

        self.assertEqual(status_icon(streamer), 'arrow-down-circle')

    def test_status_icon_non_recording(self):
        """Test status_icon when streamer is not recording."""
        streamer = Mock()
        streamer.recording = False

        # Test PUBLIC status
        streamer.sc = Status.PUBLIC
        self.assertEqual(status_icon(streamer), 'eye')

        # Test OFFLINE status
        streamer.sc = Status.OFFLINE
        self.assertEqual(status_icon(streamer), 'video-off')

        # Test UNKNOWN status
        streamer.sc = Status.UNKNOWN
        self.assertEqual(status_icon(streamer), 'help-circle')

    def test_status_icon_missing_status(self):
        """Test status_icon when streamer status is not mapped or None."""
        streamer = Mock()
        streamer.recording = False

        # Test missing status (None)
        streamer.sc = None
        self.assertEqual(status_icon(streamer), 'help-circle')

        # Test unmapped/arbitrary status not in status_icons_lookup
        streamer.sc = "SOME_UNMAPPED_STATUS"
        self.assertEqual(status_icon(streamer), 'help-circle')

if __name__ == '__main__':
    unittest.main()
