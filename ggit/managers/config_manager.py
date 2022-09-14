import json
import os
from pathlib import Path
from typing import Dict

from ggit.exceptions import ConfigException, RepositoryException
from ggit.utils import SingletonMeta
from ggit.utils.constants import repo_folder
from ggit.utils.folder_utils import find_repo_root


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

    __repo_path: Path
    __config_file: Path
    __config: Dict[str, str] = {}

    def __init__(self, repo_path: Path = None):
        repo_root = find_repo_root(Path(os.getcwd()))
        if repo_path is None and repo_root is None:
            raise RepositoryException("Not a ggit repository, (or any of the parent directories)")
        self.__repo_path = repo_path if repo_path else repo_root
        self.__config_file = self.__repo_path / repo_folder / "config.json"

        if not self.__config_file.parent.exists():
            raise ConfigException("Not a ggit repository")

        if not self.__config_file.exists():
            self.__config_file.touch()
            self.__save_config()
        else:
            self.__load_config()

    @property
    def config(self):
        return self.__config

    @property
    def repo_path(self):
        return self.__repo_path

    def __load_config(self):
        with open(self.__config_file, "r") as f:
            self.__config = json.load(f)

    def __save_config(self):
        with open(self.__config_file, "w") as f:
            json.dump(self.__config, f, indent=4)

    def __getitem__(self, key):
        if key not in self.__config:
            raise ConfigException(f'Configuration parameter "{key}" not set')
        return self.__config[key]

    def __setitem__(self, key, value):
        self.__config[key] = value
        self.__save_config()

    def __delitem__(self, key):
        del self.__config[key]
        self.__save_config()
