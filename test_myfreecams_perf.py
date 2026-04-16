import time
import unittest
from unittest.mock import patch, MagicMock
from streamonitor.sites.myfreecams import MyFreeCams
from streamonitor.enums import Status

class TestMyFreeCamsPerf(unittest.TestCase):
    @patch('streamonitor.sites.myfreecams.Bot.__init__', return_value=None)
    def test_perf(self, mock_init):
        mfc = MyFreeCams('test_user')
        mfc.username = 'test_user'
        mfc.session = MagicMock()
        mfc.logger = MagicMock()
        mfc.getVideoUrl = MagicMock(return_value="http://video")

        mock_response = MagicMock()
        mock_response.status_code = 200
        # Create a huge document
        huge_doc = b'<html>' + b'<div>dummy</div>'*1000 + b'<a href="https://www.myfreecams.com/php/tracking.php?model_id=123">link</a><div class="campreview" data-cam-preview-server-id-value="123"></div></html>'
        mock_response.content = huge_doc
        mfc.session.get.return_value = mock_response

        # warm up
        mfc.getStatus()

        start = time.time()
        for _ in range(50):
            mfc.getStatus()
        duration = time.time() - start
        print(f"\\nTime taken for 50 requests: {duration:.4f}s")

if __name__ == '__main__':
    unittest.main()
