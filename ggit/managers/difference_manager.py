import json
from pathlib import Path
from typing import Dict

from ggit.entities import Blob
from ggit.exceptions import ConfigException
from ggit.utils import Folder, SingletonMeta
from ggit.utils.constants import repo_folder


class DifferenceManager():

    __folder: Folder
    __root: Path
    __files: Dict[str, str] = {}
    __diff_files: Dict[Path, str] = {}

    def __init__(self, repo_path: Path) -> None:

        self.__folder = Folder(repo_path)
        self.__root = repo_path

        if not (self.__root / repo_folder).exists():
            raise ConfigException("Not a ggit repository")

        if (self.__root / repo_folder / "current_state.json").exists():
            try:
                with open(self.__root / repo_folder / "current_state.json", "r") as f:
                    self.__files = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

    def __get_difference(self) -> Dict[str, str]:
        temp_dict: Dict[Path, str] = {}
        for i in self.__folder.get_all_files():
            if Blob(i.read_bytes()).hash != self.__files[str(i)]:
                temp_dict[str(i)] = Blob(i.read_bytes()).hash
        return temp_dict

    @property
    def files(self) -> Dict[str, str]:
        return self.__files

    @property
    def different_files(self) -> Dict[Path, str]:
        self.__diff_files = self.__get_difference()
        return self.__diff_files

    def update_current_state(self) -> None:
        for i in self.__folder.get_all_files():
            self.__files[str(i)] = Blob(i.read_bytes()).hash

        self.__dump()

    def __dump(self) -> None:
        with open(self.__root / repo_folder / "current_state.json", "w") as f:
            json.dump(self.__files, f, indent=4)