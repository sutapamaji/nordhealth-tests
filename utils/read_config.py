import json
import os

class AppConfiguration:
    def __init__(self, config_file="config.json", env_file="environments/envs.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(base_dir, config_file)
        self.env_path = os.path.join(base_dir, env_file)
        
        self.config_data = self._load_json(self.config_path)
        self.env_data = self._load_json(self.env_path)
        
        self.current_env = self.config_data.get("Environment", "staging")
        self.base_url = self.env_data.get(self.current_env, {}).get("applicationurl")
        
        if not self.base_url:
            raise ValueError(f"URL not found for environment: {self.current_env}")

    def _load_json(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "r") as file:
            return json.load(file)

    def get(self, key: str, default=None):
        if key == "URL":
            return self.base_url
        return self.config_data.get(key, default)

config = AppConfiguration()

def get_config_value(key: str, default=None):
    return config.get(key, default)
