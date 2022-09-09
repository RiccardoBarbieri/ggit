
from pathlib import Path
from typing import Dict, List, Tuple
from pprint import pprint
import fnmatch
import re

class Folder:

    __root: Path
    __folder: Dict[str, Dict] = {}
    __ignore_file: Path
    __ignore_list: Tuple[str] = ()
    
    def __init__(self, root: Path) -> None:
        if not root.is_dir():
            raise NotADirectoryError(f"{root} is not a directory")
        self.__root = root

        self.__ignore_file = self.__root / '.ggitignore'
        if self.__ignore_file.exists():
            self.__ignore_list = tuple(self.__ignore_file.read_text().splitlines())
        self.__ignore_list += ('.ggit',)
        
        self.__folder = self.__load_folder(self.__root)

    def __load_folder(self, path: Path) -> Dict[str, Dict]:
        temp_dict: Dict[str, Dict] = {}
        for i in path.iterdir():
            if not self.__match_ignore(i):
                if i.is_dir():
                    temp_dict[i.name] = self.__load_folder(i)
                else:
                    temp_dict[i.name] = None
        return temp_dict
    
    @property
    def folder(self) -> Dict[str, Dict]:
        self.__folder = self.__load_folder(self.__root)
        return self.__folder
    
    def get_all_files(self) -> List[Path]:
        return self.__get_all_files(self.__folder, self.__root)

    def __get_all_files(self, folder: Dict[str, Dict], current_root: Path) -> List[Path]:
        temp_list: List[Path] = []
        for i in folder:
            if folder[i] is None:
                temp_list.append(current_root / i)
            else:
                temp_list.extend(self.__get_all_files(folder[i], current_root / i))
        return temp_list

    def __match_ignore(self, path: Path) -> bool:
        for i in self.__ignore_list:
            if fnmatch.fnmatch(path.name, i):
                return True
        return False
