import json
from pathlib import Path
from typing import Dict

from ggit.entities import Blob
from ggit.exceptions import ConfigException
from ggit.utils import Folder, SingletonMeta
from ggit.utils.constants import repo_folder


class DifferenceManager(metaclass=SingletonMeta):

    __folder: Folder
    __root: Path
    __files: Dict[str, str] = {}
    __diff_files: Dict[Path, str] = {}

    def __init__(self, repo_path: Path) -> None:

        self.__folder = Folder(repo_path)
        self.__root = repo_path

        if not (self.__root / repo_folder).exists():
            raise ConfigException("Not a ggit repository")

        self.__files = json.load(
            open(self.__root / repo_folder / "current_state.json", "r")
        )

    def __get_difference(self) -> Dict[Path, str]:
        temp_dict: Dict[Path, str] = {}
        for i in self.__folder.get_all_files():
            if Blob(i.read_bytes()).hash != self.__files[str(i)]:
                temp_dict[i] = Blob(i.read_bytes()).hash
        return temp_dict

    @property
    def files(self) -> Dict[Path, str]:
        return self.__files

    @property
    def different_files(self) -> Dict[Path, str]:
        self.__diff_files = self.__get_difference()
        return self.__diff_files

    def update_current_state(self) -> None:
        for i in self.__folder.get_all_files():
            self.__files[str(i)] = Blob(i.read_bytes()).hash
        json.dump(
            self.__files,
            open(self.__root / repo_folder / "current_state.json", "w"),
            indent=4,
        )

    # def __getitem__(self, key: Path) -> str:
    #     return self.__files[str(key)]

    # def __setitem__(self, key: Path, value: str) -> None:
    #     self.__files[str(key)] = value

    # def __delitem__(self, key: Path) -> None:
    #     del self.__files[str(key)]
