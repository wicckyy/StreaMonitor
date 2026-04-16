import unittest
import importlib.util
import sys
import os

class TestConfirmDeletes(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)

        # We need to test without triggering full application import sequence because we do not have external modules like Flask installed
        # The memory notes say: "To test utility functions without triggering missing external dependencies (like Flask) imported by the package's __init__.py files, use importlib.util for dynamic module loading in test files."

        # Load parameters explicitly
        class MockEnv:
            def str(self, *args, **kwargs): return args[1] if len(args) > 1 else ""
            def float(self, *args, **kwargs): return args[1] if len(args) > 1 else 0.0
            def bool(self, *args, **kwargs): return args[1] if len(args) > 1 else False
            def int(self, *args, **kwargs): return args[1] if len(args) > 1 else 0

            @classmethod
            def read_env(cls, *args, **kwargs): pass

        class MockEnviron:
            Env = MockEnv

        self.original_environ = sys.modules.get('environ')
        sys.modules['environ'] = MockEnviron

        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        import parameters
        self.original_config = parameters.WEB_CONFIRM_DELETES

        file_path = os.path.join(project_root, 'streamonitor', 'managers', 'httpmanager', 'utils', 'confirm_deletes.py')

        # Using importlib specifically as instructed in memory guidelines to avoid package __init__.py issues
        spec = importlib.util.spec_from_file_location('confirm_deletes_util', file_path)
        self.cd_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.cd_module)

    def tearDown(self):
        # Restore environ module
        if self.original_environ is not None:
            sys.modules['environ'] = self.original_environ
        else:
            sys.modules.pop('environ', None)

    def test_desktop_user_agent_mobile_config(self):
        """Test desktop UA when config is MOBILE (should not confirm delete)"""
        self.cd_module.WEB_CONFIRM_DELETES = "MOBILE"
        desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        result = self.cd_module.confirm_deletes(desktop_ua)
        self.assertFalse(result)

    def test_mobile_user_agent_mobile_config(self):
        """Test mobile UA when config is MOBILE (should confirm delete)"""
        self.cd_module.WEB_CONFIRM_DELETES = "MOBILE"
        iphone_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        result = self.cd_module.confirm_deletes(iphone_ua)
        self.assertTrue(result)

    def test_desktop_user_agent_true_config(self):
        """Test desktop UA when config is TRUE (should confirm delete)"""
        self.cd_module.WEB_CONFIRM_DELETES = "TRUE"
        desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        result = self.cd_module.confirm_deletes(desktop_ua)
        self.assertTrue(result)

    def test_desktop_user_agent_false_config(self):
        """Test desktop UA when config is FALSE (should not confirm delete)"""
        self.cd_module.WEB_CONFIRM_DELETES = "" # Empty string or False
        desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        result = self.cd_module.confirm_deletes(desktop_ua)
        self.assertFalse(result)
