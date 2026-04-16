import unittest
from unittest.mock import patch, MagicMock
import sys
import importlib.util

# Mock dependencies that might be missing in the environment or cause side effects
for module_name in ['environ', 'flask', 'm3u8', 'ffmpy', 'websocket', 'zmq', 'pycurl', 'parameters', 'requests']:
    if module_name not in sys.modules:
        sys.modules[module_name] = MagicMock()

def load_confirm_deletes():
    """Manually load confirm_deletes to bypass complex package imports."""
    module_name = 'streamonitor.managers.httpmanager.utils.confirm_deletes'
    file_path = 'streamonitor/managers/httpmanager/utils/confirm_deletes.py'
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

confirm_deletes_module = load_confirm_deletes()
confirm_deletes = confirm_deletes_module.confirm_deletes

class TestConfirmDeletes(unittest.TestCase):

    def test_always_confirm(self):
        """Test cases where WEB_CONFIRM_DELETES is set to a truthy value other than 'MOBILE'."""
        with patch.object(confirm_deletes_module, 'WEB_CONFIRM_DELETES', "True"):
            self.assertTrue(confirm_deletes("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."))
            self.assertTrue(confirm_deletes("Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) ..."))

    def test_mobile_only_confirm(self):
        """Test cases where WEB_CONFIRM_DELETES is set to 'MOBILE'."""
        with patch.object(confirm_deletes_module, 'WEB_CONFIRM_DELETES', "MOBILE"):
            # Desktop should not confirm
            self.assertFalse(confirm_deletes("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."))

            # Mobile devices should confirm
            self.assertTrue(confirm_deletes("android"))
            self.assertTrue(confirm_deletes("iphone"))
            self.assertTrue(confirm_deletes("ipad"))
            self.assertTrue(confirm_deletes("mobile"))

    def test_never_confirm(self):
        """Test cases where WEB_CONFIRM_DELETES is set to a falsy value."""
        # Empty string
        with patch.object(confirm_deletes_module, 'WEB_CONFIRM_DELETES', ""):
            self.assertFalse(confirm_deletes("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."))
            self.assertFalse(confirm_deletes("Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) ..."))

        # None
        with patch.object(confirm_deletes_module, 'WEB_CONFIRM_DELETES', None):
            self.assertFalse(confirm_deletes("Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) ..."))

if __name__ == '__main__':
    unittest.main()
