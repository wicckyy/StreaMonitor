import unittest
from streamonitor.enums import Status
from streamonitor.managers.httpmanager.mappers import web_status_lookup
from streamonitor.managers.httpmanager.filters import status_text

class TestFilters(unittest.TestCase):
    def test_status_text_valid(self):
        result = status_text(Status.PUBLIC)
        self.assertEqual(result, "Online")

    def test_status_text_invalid(self):
        result = status_text("DUMMY_STATUS")
        self.assertEqual(result, web_status_lookup[Status.OFFLINE])

    def test_status_text_falsy(self):
        result = status_text(None)
        self.assertEqual(result, web_status_lookup[Status.UNKNOWN])

if __name__ == '__main__':
    unittest.main()
