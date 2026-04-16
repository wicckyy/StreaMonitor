import unittest
from unittest.mock import patch
from streamonitor.managers.httpmanager.utils.confirm_deletes import confirm_deletes

class TestConfirmDeletes(unittest.TestCase):
    @patch('streamonitor.managers.httpmanager.utils.confirm_deletes.WEB_CONFIRM_DELETES', True)
    def test_confirm_deletes_always_true(self):
        self.assertTrue(confirm_deletes("Some Desktop Browser"))
        self.assertTrue(confirm_deletes("Android Mobile"))

    @patch('streamonitor.managers.httpmanager.utils.confirm_deletes.WEB_CONFIRM_DELETES', False)
    def test_confirm_deletes_always_false(self):
        self.assertFalse(confirm_deletes("Some Desktop Browser"))
        self.assertFalse(confirm_deletes("Android Mobile"))

    @patch('streamonitor.managers.httpmanager.utils.confirm_deletes.WEB_CONFIRM_DELETES', "MOBILE")
    def test_confirm_deletes_mobile_only(self):
        # Mobile User Agents
        self.assertTrue(confirm_deletes("Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"))
        self.assertTrue(confirm_deletes("Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1"))
        self.assertTrue(confirm_deletes("Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"))
        self.assertTrue(confirm_deletes("Generic Mobile User Agent"))

        # Non-Mobile User Agents
        self.assertFalse(confirm_deletes("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"))
        self.assertFalse(confirm_deletes("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"))

if __name__ == "__main__":
    unittest.main()
