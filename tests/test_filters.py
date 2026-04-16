import unittest
from streamonitor.enums import Status
from streamonitor.managers.httpmanager.filters import status_icon

class DummyStreamer:
    def __init__(self, recording=False, sc=Status.UNKNOWN):
        self.recording = recording
        self.sc = sc

class TestFilters(unittest.TestCase):
    def test_status_icon_recording(self):
        # When recording is True, should return 'arrow-down-circle'
        streamer = DummyStreamer(recording=True, sc=Status.PUBLIC)
        self.assertEqual(status_icon(streamer), 'arrow-down-circle')

    def test_status_icon_not_recording_known_status(self):
        # When recording is False, should return mapped icon for status
        streamer = DummyStreamer(recording=False, sc=Status.PUBLIC)
        self.assertEqual(status_icon(streamer), 'eye')

        streamer_offline = DummyStreamer(recording=False, sc=Status.OFFLINE)
        self.assertEqual(status_icon(streamer_offline), 'video-off')

    def test_status_icon_not_recording_unknown_status(self):
        # When recording is False and status not in lookup (or is UNKNOWN),
        # should return default UNKNOWN icon
        streamer = DummyStreamer(recording=False, sc=Status.UNKNOWN)
        self.assertEqual(status_icon(streamer), 'help-circle')

        # Test with a status that has no icon mapped, if applicable
        # (Though all current enum values have mapping, testing None as sc)
        streamer_none = DummyStreamer(recording=False, sc=None)
        self.assertEqual(status_icon(streamer_none), 'help-circle')

if __name__ == '__main__':
    unittest.main()
