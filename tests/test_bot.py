import unittest
from unittest.mock import MagicMock, patch
from streamonitor.bot import Bot

class TestBot(Bot):
    site = "TestSite"
    siteslug = "testsite"
    def getWebsiteURL(self):
        return f"https://testsite.com/{self.username}"

class TestBotSetUsername(unittest.TestCase):
    def setUp(self):
        self.bot = TestBot("old_username")

    @patch.object(TestBot, 'getLogger')
    @patch.object(TestBot, 'cache_file_list')
    @patch.object(TestBot, 'getWebsiteURL')
    def test_set_username_updates_attributes(self, mock_getWebsiteURL, mock_cache_file_list, mock_getLogger):
        # Setup mocks
        mock_logger = MagicMock()
        mock_getLogger.return_value = mock_logger
        mock_getWebsiteURL.return_value = "https://testsite.com/new_username"

        # Call the method
        self.bot.setUsername("new_username")

        # Verify side effects
        self.assertEqual(self.bot.username, "new_username")
        mock_getLogger.assert_called_once()
        self.assertEqual(self.bot.logger, mock_logger)
        mock_cache_file_list.assert_called_once()
        mock_getWebsiteURL.assert_called_once()
        self.assertEqual(self.bot.url, "https://testsite.com/new_username")

if __name__ == '__main__':
    unittest.main()
