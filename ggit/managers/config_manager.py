import json
import os
from pathlib import Path
from typing import Dict

from ggit.exceptions import ConfigException
from ggit.utils import SingletonMeta


class ConfigManager(metaclass=SingletonMeta):

    """
    This class represents the configuration manager for the ggit application.
    It is a singleton class, so it can be accessed from anywhere in the application and
    the instance will be the same.

    The configuration is stored in a JSON file in the .ggit placed in the folder
    where the application is executed. If the file or the folder do not exist,
    they will be created.

    The configuration is loaded when the class is instantiated and saved when
    the configuration is modified.

    This class implements the methods __getitem__, __setitem__ and __delitem__ to
    access the configuration as if it were a dictionary.
    To delete a configuration parameter, use the "del" operator.

    Example:
        config = ConfigManager()
        config['user.name'] = 'John Doe'
        print(config['user.name'])
        del config['user.name']
    
    Attributes
    ----------
    config_file : Path
        The path to the configuration file.
    config : Dict[str, str]
        The configuration dictionary.
    """

    __repo_path: Path = Path(os.getcwd())
    config_file: Path = __repo_path / '.ggit' / 'config.json'
    config: Dict[str, str] = {}

    def __init__(self):
        if not self.config_file.exists():
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config_file.touch()
            self.__save_config()
        else:
            self.__load_config()

    def __load_config(self):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def __save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def __getitem__(self, key):
        if key not in self.config:
            raise ConfigException(f'Configuration parameter "{key}" not set')
        return self.config[key]
    
    def __setitem__(self, key, value):
        self.config[key] = value
        self.__save_config()
    
    def __delitem__(self, key):
        del self.config[key]
        self.__save_config()
