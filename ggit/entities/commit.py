import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ggit.entities import User

from ggit.entities import Blob, Tree
from ggit.utils import walk_folder_flat


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
    author NameOfAuthor <email@example.com> 1662040308 +0200
    committer name <email@example.com> 1662040308 +0200

    commit message

    """

    __tree: Tree
    __parent: 'Commit | None'
    __date_time: datetime
    __author: 'User'
    __committer: 'User'
    __message: str
    __hash: str
    __body: bytes

    def __init__(self, tree: Tree = None, parent: 'Commit | None' = None, __date_time: datetime = None, author: 'User' = None, committer: 'User' = None, message: str = None):
        self.__tree = tree
        self.__parent = parent
        self.__date_time = __date_time
        self.__author = author
        self.__committer = committer
        self.__message = message

    @property
    def tree(self) -> Tree:
        return self.__tree

    @tree.setter
    def tree(self, tree: Tree):
        self.__tree = tree

    @property
    def parent(self) -> 'Commit | None':
        return self.__parent

    @parent.setter
    def parent(self, parent: 'Commit | None'):
        self.__parent = parent

    @property
    def date_time(self) -> datetime:
        return self.__date_time

    @date_time.setter
    def date_time(self, date_time: datetime):
        self.__date_time = date_time

    @property
    def author(self) -> 'User':
        return self.__author

    @author.setter
    def author(self, author: 'User'):
        self.__author = author

    @property
    def committer(self) -> 'User':
        return self.__committer

    @committer.setter
    def committer(self, committer: 'User'):
        self.__committer = committer

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, message: str):
        self.__message = message

    @property
    def hash(self) -> str:
        self.__hash = self.__calculate_hash()
        return self.__hash

    def __compose_body(self) -> str:
        self.__body = b""
        try:
            self.__body = b"tree " + self.tree.hash.encode('ascii') + b"\n"
        except AttributeError:
            raise AttributeError("The commit must have a parent tree")
        if self.parent is not None:
            self.__body += b"parent " + self.parent.hash.encode('ascii') + b"\n"
        try:
            self.__body += b"author " + str(self.author).encode('ascii') + b" " + str(int(self.date_time.timestamp())).encode('ascii') + b" " + str(self.date_time.astimezone())[-6:].replace(':', '').encode('ascii') + b"\n"
        except AttributeError:
            raise AttributeError("The commit must have an author")
        try:
            self.__body += b"committer " + str(self.committer).encode('ascii') + b" " + str(int(self.date_time.timestamp())).encode('ascii') + b" " + str(self.date_time.astimezone())[-6:].replace(':', '').encode('ascii') + b"\n"
        except AttributeError:
            raise AttributeError("The commit must have an author")
        self.__body += b"\n" + self.message.encode('ascii') + b"\n"

    def __calculate_hash(self) -> str:
        self.__compose_body()
        return hashlib.sha1(b"commit " + str(len(self.__body)).encode('ascii') + b"\0" + self.__body).hexdigest()


if __name__ == "__main__":
    from ggit.entities import User
    repo = Path(__file__).parent.parent.joinpath('test', 'assets', 'tree_tester')

    items_sub = []
    for i in walk_folder_flat(repo.joinpath('sub')):
        if os.access(i, os.X_OK):
            mode = '100755'
        elif i.is_symlink():
            mode = '120000'
        else:
            mode = '100644'
        items_sub.append((Blob(i.read_bytes()), i.name, mode))

    sub_tree = Tree(items_sub)
    items_main = []
    for i in walk_folder_flat(repo):
        if os.access(i, os.X_OK):
            mode = '100755'
        elif i.is_symlink():
            mode = '120000'
        else:
            mode = '100644'
        items_main.append((Blob(i.read_bytes()), i.name, mode))
    items_main.append((sub_tree, 'sub', '040000'))
    main_tree = Tree(items_main)

    commit = Commit()

    commit.tree = main_tree
    commit.parent = None
    date_time = datetime.fromtimestamp(1662113769)
    commit.date_time = date_time
    commit.author = User('RiccardoBarbieri', 'riccardo_barbieri@outlook.it')
    commit.committer = User('RiccardoBarbieri', 'riccardo_barbieri@outlook.it')
    commit.message = 'test'

    print(commit.hash)