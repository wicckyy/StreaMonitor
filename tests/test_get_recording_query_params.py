import unittest
import importlib.util
import os

# Define the path to the module
# We use a relative path from the test file to the source file
base_dir = os.path.dirname(__file__)
module_path = os.path.join(base_dir, '../streamonitor/managers/httpmanager/utils/get_recording_query_params.py')
module_path = os.path.abspath(module_path)

# Load the module dynamically to avoid dependency issues with the parent package.
# This utility function is a pure function and doesn't depend on other modules in the package.
# Importing it via the package would require mocking numerous missing dependencies (flask, m3u8, etc.)
spec = importlib.util.spec_from_file_location("get_recording_query_params_mod", module_path)
get_recording_query_params_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(get_recording_query_params_mod)
get_recording_query_params = get_recording_query_params_mod.get_recording_query_params

class TestGetRecordingQueryParams(unittest.TestCase):
    def test_no_params(self):
        result = get_recording_query_params(False, None)
        self.assertEqual(result, "")

    def test_sort_by_size_only(self):
        result = get_recording_query_params(True, None)
        self.assertEqual(result, "?sorted=True")

    def test_current_video_only(self):
        result = get_recording_query_params(False, "video123")
        self.assertEqual(result, "?play_video=video123")

    def test_both_params(self):
        result = get_recording_query_params(True, "video123")
        self.assertEqual(result, "?sorted=True&play_video=video123")

if __name__ == '__main__':
    unittest.main()
