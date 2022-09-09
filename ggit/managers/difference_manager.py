import os
from pathlib import Path
from pprint import pprint
from typing import Dict
from ggit.utils import SingletonMeta, Folder
from ggit.utils.folder_utils import walk_folder_rec_flat
from ggit.entities import Blob
import json


class DifferenceManager(metaclass=SingletonMeta):

    __folder: Folder = Folder(Path(os.getcwd()))
    __root: Path = Path(os.getcwd())
    __files: Dict[str, str] = {}
    __diff_files: Dict[Path, str] = {}

    def __init__(self) -> None:
        self.__files = json.load(
            open(self.__root / ".ggit" / "current_state.json", "r")
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
            open(self.__root / ".ggit" / "current_state.json", "w"),
            indent=4,
        )

    def __getitem__(self, key: Path) -> str:
        return self.__files[key]

    def __setitem__(self, key: Path, value: str) -> None:
        self.__files[key] = value

    def __delitem__(self, key: Path) -> None:
        del self.__files[key]




