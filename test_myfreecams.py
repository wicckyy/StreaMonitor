import unittest
from unittest.mock import patch, MagicMock
from streamonitor.sites.myfreecams import MyFreeCams
from streamonitor.enums import Status
from streamonitor.bot import Bot

# Make sure tests run without hanging on init
class MockBot(Bot):
    siteslug = 'MFC'
    def __init__(self, username):
        # Avoid thread starting
        self.username = username
        self.session = MagicMock()
        self.logger = MagicMock()
        self.attrs = {}
        self.videoUrl = None

@patch('streamonitor.sites.myfreecams.Bot.__init__', return_value=None)
class TestMyFreeCams(unittest.TestCase):
    def test_get_status_public(self, mock_init):
        # We patch __init__ because Bot.__init__ tries to start a thread/etc
        mfc = MyFreeCams('test_user')
        mfc.username = 'test_user'
        mfc.session = MagicMock()
        mfc.logger = MagicMock()
        mfc.getVideoUrl = MagicMock(return_value="http://video")

        # Mocking the share response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><a href="https://www.myfreecams.com/php/tracking.php?model_id=123">link</a><div class="campreview" data-cam-preview-server-id-value="123"></div></html>'
        mfc.session.get.return_value = mock_response

        status = mfc.getStatus()
        self.assertEqual(status, Status.PUBLIC)

if __name__ == '__main__':
    unittest.main()
