import unittest
from unittest.mock import patch, MagicMock

from streamonitor.bot import Bot


class MockBot(Bot):
    siteslug = 'test_slug'
    site = 'test_site'

    def __init__(self, username):
        # Do not call super().__init__ to avoid Thread initialization issues
        # and dependencies on requests.Session etc., just initialize needed variables.
        self.username = username
        self.siteslug = 'test_slug'
        self.running = False


class TestBot(unittest.TestCase):
    def test_restart(self):
        bot = MockBot('test_user')
        self.assertFalse(bot.running)

        bot.restart()
        self.assertTrue(bot.running)


if __name__ == '__main__':
    unittest.main()
