import json
from pathlib import Path
from typing import Dict

from ggit.entities import Blob
from ggit.exceptions import ConfigException
from ggit.utils.constants import repo_folder


class StashManager:

    __root: Path
    __stashed_files: Dict[Path, str] = {}

    def __init__(self, repo_path: Path) -> None:

        self.__root = repo_path

        if not (self.__root / repo_folder).exists():
            raise ConfigException("Not a ggit repository")

        self.__stashed_files = json.load(
            open(self.__root / repo_folder / "stash.json", "r")
        )

    def stash_file(self, file_path: Path) -> None:
        self.__stashed_files[file_path] = Blob(file_path.read_bytes()).hash
        json.dump(
            self.__stashed_files,
            open(self.__root / repo_folder / "stash.json", "w"),
            indent=4,
        )

    def unstash_file(self, file_path: Path) -> None:
        del self.__stashed_files[file_path]
        json.dump(
            self.__stashed_files,
            open(self.__root / repo_folder / "stash.json", "w"),
            indent=4,
        )

    @property
    def stashed_files(self) -> Dict[Path, str]:
        return self.__stashed_files
