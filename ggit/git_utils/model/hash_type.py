import os
from enum import Enum
from pathlib import Path
from typing import List

from ggit.git_utils.git_connector import (GitConnectorInterface, GitConnectorSubprocess)
from ggit.utils.folder_utils import walk_objects


class HashType(Enum):

    """
    Enum class that defines the different hash types.

    Attributes
    ----------
    COMMIT: str
        The hash type for a commit.
    TREE: str
        The hash type for a tree.
    BLOB: str
        The hash type for a blob.
    """

    BLOB = 0
    TREE = 1
    COMMIT = 2

class GitHash:

    """
    Class that represent a git hash, associating the sha1 hash string with the
    type of hash, the path of the file and the path to the repository.

    Attributes
    ----------
    __hash: str
        The sha1 hash string.
    __type: :class:`HashType`
        The type of hash.
    __path: str
        The path of the file.
    __repo: str
        The path to the repository.
    
    Parameters
    ----------
    hash: str
        The sha1 hash string.
    type: :class:`HashType`
        The type of hash.
    path: str
        The path of the file.
    repo: str
        The path to the repository.
    """

    __hash: str = ''
    __type: HashType = None

    __path: str = ''
    __repo: str = ''

    def __init__(self, hash: str, type: HashType, path: str, repo: str):
        self.__hash = hash
        self.__type = type
        self.__path = path
        self.__repo = repo

    @property
    def hash(self) -> str:
        return self.__hash

    @property
    def type(self) -> HashType:
        return self.__type

    @property
    def repo(self) -> str:
        return self.__repo
    
    @property
    def path(self) -> str:
        return self.__path

    def __str__(self) -> str:
        return f'<{self.hash}, {self.type}>'



class HashIdentifier:

    """
    Class used to obtain the hashes of the repository and their type, creating
    a list of :class:`GitHash` objects.

    Parameters
    ----------
    repository: str, optional
        The repository to obtain the hashes from.
    """

    __files: List[Path] = []
    __hashes: List[GitHash] = []
    
    def __init__(self, repository = '/home/riccardoob/thesis/git_test'):
        self.repository = repository
        try:
            os.chdir(repository)
        except FileNotFoundError:
            print('Directory not found')
            raise FileNotFoundError(f'{repository} is not a directory.')

    def __get_all_objects(self) -> List[Path]:
        """
        Method that walks the repository .git/objects folder and a list of
        Path objects, containing the paths of all the objects found.

        Returns
        -------
        List[Path]
            The list of Path objects of the git objects found.
        """
        raw_list = walk_objects(Path.joinpath(Path(self.repository)))
        self.__files = raw_list
        return self.__files
    
    def __get_all_hashes(self) -> List[GitHash]:
        """
        Method that obtains the hashes of the repository and their type,
        creating a list of :class:`GitHash` objects.
        """
        self.__get_all_objects()
        
        for file in self.__files:
            hash_ = ''.join(str(file).split('/')[-2:])

            conn: GitConnectorInterface = GitConnectorSubprocess()
            hash_type = conn.get_hash_type(hash_)

            self.__hashes.append(
                GitHash(
                    hash_,
                    hash_type,
                    file,
                    self.repository
                )
            )
    
    def get_hashes(self) -> List[GitHash]:
        """
        Method that calls the __get_all_hashes method and returns the list of
        :class:`GitHash` objects.

        Returns
        -------
        List[:class:`GitHash`]
            The list of :class:`GitHash` objects.
        """
        self.__get_all_hashes()
        return self.__hashes

# if __name__ == '__main__':
#     hash_identifier = HashIdentifier()
#     hashes = hash_identifier.get_hashes()

