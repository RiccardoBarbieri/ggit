import json
import os
from pathlib import Path
from typing import Dict

from ggit.exceptions import ConfigException
from ggit.utils import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):

    repo_path: Path = Path(os.getcwd())
    config_file: Path = repo_path / '.ggit' / 'config.json'
    config: Dict[str, str] = {}

    def __init__(self):
        if not self.config_file.exists():
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config_file.touch()
            self.save_config()
        else:
            self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def __getitem__(self, key):
        if key not in self.config:
            raise ConfigException(f'Configuration parameter "{key}" not set')
        return self.config[key]
    
    def __setitem__(self, key, value):
        self.config[key] = value
        self.save_config()
    
    def __delitem__(self, key):
        del self.config[key]
        self.save_config()
