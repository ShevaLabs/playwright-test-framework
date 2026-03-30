import os
import yaml
from pathlib import Path
from typing import Dict, Any

class EnvironmentConfig:
    def __init__(self, env: str = "dev"):
        self.env = env
        self.config = self._load_config()
        self.env_config = self.config["environments"][env]

    def _load_config(self) -> Dict[str, Any]:
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Override with environment variables
        for key, value in config.get("environments", {}).get(self.env, {}).items():
            env_var = os.getenv(key.upper())
            if env_var:
                config["environments"][self.env][key] = env_var

        return config

    @property
    def base_url(self) -> str:
        return self.env_config["base_url"]

    @property
    def api_url(self) -> str:
        return self.env_config["api_url"]

    @property
    def username(self) -> str:
        return self.env_config["username"]

    @property
    def password(self) -> str:
        return self.env_config["password"]

    def get_playwright_config(self) -> Dict[str, Any]:
        return self.config.get("playwright", {})

    def get_test_config(self) -> Dict[str, Any]:
        return self.config.get("test", {})