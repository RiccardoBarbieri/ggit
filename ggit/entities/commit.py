import hashlib
from datetime import datetime, timedelta, timezone
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
    author NameOfAuthor <email@example.com> 1662040308 +0200
    committer NameOfCommitter <email@example.com> 1662040308 +0200

    commit message

    Attributes
    ----------
    tree : Tree
        The main tree of the commit.
    parent : Commit | None
        The parent of the commit, if the commit is the first commit of the repository
        the parent is None.
    date_time : datetime
        The date and time of the commit.
    str_date_time : str
        The date and time of the commit in a string format.
        Format: UNIX-timestamp +0000
    author : User
        The author of the commit.
    committer : User
        The committer of the commit.
    message : str
        The message of the commit.
    hash : str
        The hash of the commit.
    content : str
        The content of the commit, the content is the body of the commit.
    length : int
        The length of the content of the commit.
    """

    __tree: Tree
    __parent: "Commit | None"
    __date_time: datetime
    __author: "User"
    __committer: "User"
    __message: str
    __hash: str
    __body: bytes

    def __init__(
        self,
        tree: Tree = None,
        parent: "Commit | None" = None,
        date_time: datetime = None,
        author: "User" = None,
        committer: "User" = None,
        message: str = None,
    ):
        self.__tree = tree
        self.__parent = parent
        self.__date_time = date_time
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
    def parent(self) -> "Commit | None":
        return self.__parent

    @parent.setter
    def parent(self, parent: "Commit | None"):
        self.__parent = parent

    @property
    def str_date_time(self) -> str:
        string = str(int(self.__date_time.timestamp())) + " " + self.__date_time.astimezone().strftime("%z")
        return string

    @str_date_time.setter
    def str_date_time(self, str_date_time: str):
        offset = timedelta(hours=int(str_date_time[-4:-2]))
        tz = timezone(offset=offset)

        self.__date_time = datetime.fromtimestamp(int(str_date_time.split(" ")[0]), tz=tz)

    @property
    def date_time(self) -> str:
        return self.__date_time

    @date_time.setter
    def date_time(self, date_time: datetime):
        self.__date_time = date_time

    @property
    def author(self) -> "User":
        return self.__author

    @author.setter
    def author(self, author: "User"):
        self.__author = author

    @property
    def committer(self) -> "User":
        return self.__committer

    @committer.setter
    def committer(self, committer: "User"):
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

    @property
    def content(self) -> bytes:
        self.__compose_body()
        return self.__body

    @property
    def length(self) -> int:
        return len(self.content)

    def __compose_body(self):
        """
        Method that creates the body of the commit.
        The body of the commit is a string containing information about the commit,
        the format is as described above.
        """
        self.__body = b""
        try:
            self.__body = b"tree " + self.tree.hash.encode("ascii") + b"\n"
        except AttributeError:
            raise AttributeError("The commit must have a parent tree")
        if self.parent is not None:
            self.__body += b"parent " + self.parent.hash.encode("ascii") + b"\n"
        try:
            self.__body += (
                b"author "
                + str(self.author).encode("ascii")
                + b" "
                + str(int(self.date_time.timestamp())).encode("ascii")
                + b" "
                + str(self.date_time.astimezone())[-6:].replace(":", "").encode("ascii")
                + b"\n"
            )
        except AttributeError:
            raise AttributeError("The commit must have an author")
        try:
            self.__body += (
                b"committer "
                + str(self.committer).encode("ascii")
                + b" "
                + str(int(self.date_time.timestamp())).encode("ascii")
                + b" "
                + str(self.date_time.astimezone())[-6:].replace(":", "").encode("ascii")
                + b"\n"
            )
        except AttributeError:
            raise AttributeError("The commit must have an author")
        self.__body += b"\n" + self.message.encode("ascii") + b"\n"

    def __calculate_hash(self) -> str:
        """
        Method that calculates the hash of the commit.
        The hash of the commit is calculated in a similar way as the tree hash,
        hashing a string containing the word "commit " followed by the size of the body
        terminated by a NUL character, followed by the body of the commit.

        Returns
        -------
        str
            The hash of the commit.
        """
        self.__compose_body()
        return hashlib.sha1(
            b"commit " + str(len(self.__body)).encode("ascii") + b"\0" + self.__body
        ).hexdigest()

    def __str__(self) -> str:
        return f"Commit: {self.hash}"

    def __repr__(self) -> str:
        return f"Commit: {self.hash}"

    def __eq__(self, other: "Commit") -> bool:
        if isinstance(other, Commit):
            return self.__hash == other.hash
        return False

    def __hash__(self) -> int:
        return self.hash
