import json
import os

class TestData:
    def __init__(self, filename="testdata.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(base_dir, "testdata", filename)
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Test data file not found: {self.data_path}")
        with open(self.data_path, "r") as file:
            return json.load(file)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

test_data = TestData()

def get_test_data(key: str, default=None):
    """ Retrieve test data values based on a key. """
    return test_data.get(key, default)
