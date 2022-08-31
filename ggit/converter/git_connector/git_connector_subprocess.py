import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Generator, List, Tuple

if TYPE_CHECKING:
    from ggit.converter.model.hash_type import HashType

from ggit.converter.git_connector.git_connector_interface import GitConnectorInterface
from ggit.utils import walk_objects


class GitConnectorSubprocess(GitConnectorInterface):
    """
    Class that implements the :class:`GitConnectorInterface` using the subprocess module
    to interact with git cli directly. To use the functionality of this class, one must
    have the git cli installed and be in the correct directory.
    """

    
    def get_hash_type(self, hash_: str) -> 'HashType':
        from ggit.converter.model.hash_type import HashType
        from ggit.process_exception import ProcessException
        """
        Obtain the :class:`HashType` of the hash provided.
        
        Parameters
        ----------
        hash: str
            The hash to obtain the type from.

        Returns
        -------
        :class:`HashType`
            The type of the hash.

        Raises
        ------
        :class:`ProcessException`
            If the process to identify the hash exits with errors.
        """
        hash_type_process = subprocess.run(['git', 'cat-file', '-t', hash_], stdout=subprocess.PIPE)
        if hash_type_process.stderr:
            raise ProcessException(hash_type_process.stderr.strip().decode('utf-8'))
            
        return HashType[hash_type_process.stdout.strip().decode('utf-8').upper()]

    def get_all_objects(self) -> Generator[Tuple[str, 'HashType'], None, None]:
        from ggit.process_exception import ProcessException
        """
        Obtain all the objects in the repository as a list of tuples that
        associates the object hash with the object type.

        Returns
        -------
        Generator[Tuple[str,:class:`HashType`], None, None]
            A generator that yields tuples that associates the object hash with the object type.
        
        Raises
        ------
        :class:`ProcessException`
            If any process exits with errors.
        """
        objects = walk_objects(os.getcwd())
        for obj in objects:
            hash_ = ''.join(str(obj).split('/')[-2:])
            hash_type = self.get_hash_type(hash_)
            yield (hash_, hash_type)

        


    def hash_object(self, path: Path) -> str:
        from ggit.process_exception import ProcessException
        """
        Obtain the hash of the object at the path provided.
        
        Parameters
        ----------
        path: str
            The path of the object to hash.

        Returns
        -------
        str
            The hash of the file provided.

        Raises
        ------
        :class:`ProcessException`
            If the process to obtain the hash exits with errors.
        """
        hash_process = subprocess.run(['git', 'hash-object', path], stdout=subprocess.PIPE)
        if hash_process.stderr:
            raise ProcessException(hash_process.stderr.strip().decode('utf-8'))
            
        return hash_process.stdout.strip().decode('utf-8')