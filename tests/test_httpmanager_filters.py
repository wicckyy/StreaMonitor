import unittest

from streamonitor.managers.httpmanager.filters import status_text
from streamonitor.enums.status import Status

class TestFilters(unittest.TestCase):
    def test_status_text_none(self):
        """Test status_text with None input"""
        self.assertEqual(status_text(None), "Unknown Error")

    def test_status_text_public(self):
        """Test status_text with expected Status enum"""
        self.assertEqual(status_text(Status.PUBLIC), "Online")

    def test_status_text_invalid(self):
        """Test status_text with invalid status value"""
        # Given 'random', it falls back to Offline
        self.assertEqual(status_text("random"), "Offline")

if __name__ == '__main__':
    unittest.main()
