import unittest
from unittest.mock import MagicMock
from streamonitor.bot import Bot

class TestBot(unittest.TestCase):
    def setUp(self):
        # We need a site slug since it's used in logging initialization during init
        Bot.siteslug = "test_slug"

    def test_stop_when_running_with_thread_too(self):
        bot = Bot("test_user")
        bot.running = True
        bot.stopDownload = MagicMock()
        bot.log = MagicMock()

        bot.stop(None, None, thread_too=True)

        bot.log.assert_called_once_with("Stopping...")
        bot.stopDownload.assert_called_once()
        self.assertFalse(bot.running)
        self.assertTrue(bot.quitting)

    def test_stop_when_not_running_with_thread_too(self):
        bot = Bot("test_user")
        bot.running = False
        bot.stopDownload = MagicMock()
        bot.log = MagicMock()

        bot.stop(None, None, thread_too=True)

        bot.log.assert_not_called()
        bot.stopDownload.assert_not_called()
        self.assertFalse(bot.running)
        self.assertTrue(bot.quitting)

    def test_stop_when_running_without_thread_too(self):
        bot = Bot("test_user")
        bot.running = True
        bot.stopDownload = MagicMock()
        bot.log = MagicMock()

        bot.stop(None, None, thread_too=False)

        bot.log.assert_called_once_with("Stopping...")
        bot.stopDownload.assert_called_once()
        self.assertFalse(bot.running)
        self.assertFalse(bot.quitting)

    def test_stop_when_not_running_without_thread_too(self):
        bot = Bot("test_user")
        bot.running = False
        bot.stopDownload = MagicMock()
        bot.log = MagicMock()

        bot.stop(None, None, thread_too=False)

        bot.log.assert_not_called()
        bot.stopDownload.assert_not_called()
        self.assertFalse(bot.running)
        self.assertFalse(bot.quitting)

    def test_stop_when_stopDownload_is_none(self):
        bot = Bot("test_user")
        bot.running = True
        bot.stopDownload = None
        bot.log = MagicMock()

        bot.stop(None, None, thread_too=False)

        bot.log.assert_called_once_with("Stopping...")
        self.assertFalse(bot.running)
        self.assertFalse(bot.quitting)

if __name__ == '__main__':
    unittest.main()
