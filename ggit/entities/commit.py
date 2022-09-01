from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ggit.entities import User

from ggit.entities import Tree

class Commit:
    """
    This class represents a commit, it contains the main tree that
    mirrors the staging area, the author, the committer and the message of the commit.
    The commit class also stores the parent of the commit, if the commit is the first 
    commit of the repository the parent is None.
    The hash of the commit is calculated in a similar way as the tree hash, hashing a string
    containing the word "commit " followed by the size of the body terminated by a NUL character,
    followed by the body of the commit.
    The body of the commit is a string containing information about the commit, the format is:
    
    tree ff7ae585339f04217663bdb7f54df531c6fb8217
    author RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200
    committer RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200

    test
    
    """

    __tree: Tree
    __parent: 'Commit | None'
    __timestamp: int
    __author: 'User'
    __committer: 'User'
    __message: str
    __hash: str
    __body: bytes

    def __init__(self, tree: Tree = None, parent: 'Commit | None' = None, timestamp: int = None, author: 'User' = None, committer: 'User' = None, message: str = None):
        self.__tree = tree
        self.__parent = parent
        self.__timestamp = timestamp
        self.__author = author
        self.__committer = committer
        self.__message = message
        # self.__hash = self.__calculate_hash()

    @property
    def tree(self) -> Tree:
        return self.__tree

    @tree.setter
    def tree(self, tree: Tree):
        self.__tree = tree
        self.__hash = self.__calculate_hash()

    @property
    def parent(self) -> 'Commit | None':
        return self.__parent

    @parent.setter
    def parent(self, parent: 'Commit | None'): 
        self.__parent = parent
        self.__hash = self.__calculate_hash()

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int):
        self.__timestamp = timestamp
        self.__hash = self.__calculate_hash()

    @property
    def author(self) -> 'User':
        return self.__author

    @author.setter
    def author(self, author: 'User'):
        self.__author = author
        self.__hash = self.__calculate_hash()

    @property
    def committer(self) -> 'User':
        return self.__committer

    @committer.setter
    def committer(self, committer: 'User'):
        self.__committer = committer
        self.__hash = self.__calculate_hash()

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, message: str):
        self.__message = message
        self.__hash = self.__calculate_hash()

    @property
    def hash(self) -> str:
        return self.__hash

    def compose_body(self) -> str:
        self.__body = b"tree " + self.tree.hash + b"\n"

a = Commit()


