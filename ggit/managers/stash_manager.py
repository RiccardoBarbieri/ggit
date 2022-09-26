import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

from ggit.entities import Blob
from ggit.entities.tree import Tree
from ggit.exceptions import ConfigException
from ggit.utils import SingletonMeta
from ggit.utils.constants import repo_folder
from ggit.utils.folder import Folder


class StashManager():

    __root: Path
    __stashed_files: Dict[str, str] = {}
    __tracked_files: List[str] = []

    def __init__(self, repo_path: Path) -> None:

        self.__root = repo_path

        if not (self.__root / repo_folder).exists():
            raise ConfigException("Not a ggit repository")

        if (self.__root / repo_folder / "stash.json").exists():
            try:
                with open(self.__root / repo_folder / "stash.json", "r") as f:
                    self.__stashed_files = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

        if (self.__root / repo_folder / "tracked_files.json").exists():
            try:
                with open(self.__root / repo_folder / "tracked_files.json", "r") as f:
                    self.__tracked_files = json.load(f)
            except json.decoder.JSONDecodeError:
                pass

    def __dump(self) -> None:
        with open(self.__root / repo_folder / "stash.json", "w+") as f:
            json.dump(
                self.__stashed_files,
                f,
                indent=4,
            )
        with open(self.__root / repo_folder / "tracked_files.json", "w+") as f:
            json.dump(
                self.__tracked_files,
                f,
                indent=4,
            )

    def stash(self, path: Path) -> None:
        if path.is_file():
            self.__stash_file(path)
        else:
            self.__stash_folder(path)

        self.__dump()

    def __stash_file(self, file_path: Path) -> None:
        self.__stashed_files[str(file_path)] = Blob(file_path.read_bytes()).hash
        if str(file_path) not in self.__tracked_files:
            self.__tracked_files.append(str(file_path))

    def __stash_folder(self, folder_path: Path) -> None:
        for i in folder_path.iterdir():
            if i.is_file():
                self.__stash_file(i)
            else:
                self.__stash_folder(i)

    def unstash(self, path: Path) -> None:
        if path.is_file():
            self.__unstash_file(path)
        else:
            self.__unstash_folder(path)

        self.__dump()

    def __unstash_file(self, file_path: Path) -> None:
        del self.__stashed_files[str(file_path)]
        os.remove(file_path)
        if str(file_path) in self.__tracked_files:
            self.__tracked_files.remove(str(file_path))

    def __unstash_folder(self, folder_path: Path) -> None:
        for i in folder_path.iterdir():
            if i.is_file():
                self.__unstash_file(i)
            else:
                self.__unstash_folder(i)
        shutil.rmtree(folder_path)

    def move(self, old_path: Path, new_path: Path) -> None:
        if old_path.is_file():
            self.__move_file(old_path, new_path)
        else:
            self.__move_folder(old_path, new_path)

        self.__dump()

    def __move_file(self, old_path: Path, new_path: Path) -> None:
        if str(old_path) in self.__stashed_files:
            self.__stashed_files[str(new_path)] = self.__stashed_files[str(old_path)]
            del self.__stashed_files[str(old_path)]
        if str(old_path) in self.__tracked_files:
            self.__tracked_files.remove(str(old_path))
            self.__tracked_files.append(str(new_path))
        os.renames(old_path, new_path)

    def __move_folder(self, old_path: Path, new_path: Path) -> None:
        for i in old_path.iterdir():
            if i.is_file():
                self.__move_file(i, new_path / i.name)
            else:
                self.__move_folder(i, new_path / i.name)
        shutil.rmtree(old_path)

    def clear_stash(self) -> None:
        for i in self.__tracked_files:
            if i in self.__stashed_files:
                del self.__stashed_files[i]
        self.__dump()

    @property
    def stashed_files(self) -> Dict[str, str]:
        return self.__stashed_files

    @property
    def tracked_files(self) -> List[str]:
        return self.__tracked_files
