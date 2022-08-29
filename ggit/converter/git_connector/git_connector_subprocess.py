import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

sys.path.append(Path(__file__).parent.parent.parent.__str__())

if TYPE_CHECKING:
    from model.hash_type import HashType

from converter.git_connector.git_connector_interface import GitConnectorInterface


class GitConnectorSubprocess(GitConnectorInterface):
    """
    Class that implements the :class:`GitConnectorInterface` using the subprocess module
    to interact with git cli directly.
    """

    
    def get_hash_type(self, hash_: str) -> 'HashType':
        from converter.model.hash_type import HashType
        from process_exception import ProcessException
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

    def hash_object(self, path: Path) -> str:
        from process_exception import ProcessException
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
