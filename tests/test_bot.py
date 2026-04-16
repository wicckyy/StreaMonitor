import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streamonitor.bot import Bot

class DummyBot(Bot):
    site = "dummy"
    siteslug = "dummy"
    def __init__(self, username):
        # We override __init__ to avoid threading.Thread instantiation issues during test
        self.username = username
        self.running = False
        self.quitting = False
        self.stopDownload = None
        self.logger = self

    def info(self, msg):
        pass

class TestBotStop(unittest.TestCase):
    def test_stop_running_thread_too_false(self):
        bot = DummyBot("testuser")
        bot.running = True

        stop_called = [False]
        def mock_stop():
            stop_called[0] = True

        bot.stopDownload = mock_stop

        bot.stop(None, None, thread_too=False)

        self.assertFalse(bot.running)
        self.assertTrue(stop_called[0])
        self.assertFalse(bot.quitting)

    def test_stop_running_thread_too_true(self):
        bot = DummyBot("testuser")
        bot.running = True

        stop_called = [False]
        def mock_stop():
            stop_called[0] = True

        bot.stopDownload = mock_stop

        bot.stop(None, None, thread_too=True)

        self.assertFalse(bot.running)
        self.assertTrue(stop_called[0])
        self.assertTrue(bot.quitting)

    def test_stop_not_running_thread_too_false(self):
        bot = DummyBot("testuser")
        bot.running = False

        stop_called = [False]
        def mock_stop():
            stop_called[0] = True

        bot.stopDownload = mock_stop

        bot.stop(None, None, thread_too=False)

        self.assertFalse(bot.running)
        self.assertFalse(stop_called[0])
        self.assertFalse(bot.quitting)

    def test_stop_not_running_thread_too_true(self):
        # The edge case
        bot = DummyBot("testuser")
        bot.running = False

        stop_called = [False]
        def mock_stop():
            stop_called[0] = True

        bot.stopDownload = mock_stop

        bot.stop(None, None, thread_too=True)

        self.assertFalse(bot.running)
        self.assertFalse(stop_called[0])
        self.assertTrue(bot.quitting)

if __name__ == '__main__':
    unittest.main()
