"""
Configuration Reader Utility
Read configuration from JSON/YAML files
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigReader:
    """Read and manage configuration"""

    _config = None

    @classmethod
    def load_config(cls, env: str = "qa") -> Dict[str, Any]:
        """Load configuration for specified environment"""
        if cls._config is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / 'Testdata' / 'config.json'

            with open(config_path) as f:
                all_config = json.load(f)

            cls._config = all_config.get(env, all_config.get('qa'))

        return cls._config

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        if cls._config is None:
            cls.load_config()
        return cls._config.get(key, default)

    @classmethod
    def get_base_url(cls) -> str:
        """Get base URL from config"""
        return cls.get('base_url')

    @classmethod
    def get_timeout(cls) -> int:
        """Get default timeout from config"""
        return cls.get('timeout', 30000)