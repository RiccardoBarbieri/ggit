import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.hash_type import HashType


class GitConnectorInterface(metaclass=abc.ABCMeta):
    """
    Interface that defines the methods that a GitConnector must implement.
    A GitConnector is a class that is used to interact with the git repository.
    """
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_hash_type') and
                callable(subclass.get_hash_type))

    @abc.abstractmethod
    def get_hash_type(self, hash: str) -> 'HashType':
        """
        Obtain the :class:`HashType` of the hash provided.
        
        Parameters
        ----------
        hash: str
            The hash to obtain the type from.
        """
        raise NotImplementedError
