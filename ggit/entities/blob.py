import hashlib

class Blob:
    """
    This class represent a BLOB (Binary Large OBject), a blob stores
    the contents of a file without keeping track of its metadata.
    In git, a blob is identified by it's sha1 hash, calculated by concatenating
    the string "blob ", an integer representing the size of the file in bytes,
    followed by a NUL character, ending with the actual content of the file.

    Attributes
    ----------
    content : str | bytes
        The content of the blob.
    length : int
        The length of the blob.
    hash : str
        The hash of the blob.

    Parameters
    ----------
    content : str | bytes
        The content of the blob.
    """

    __content: str | bytes
    __length: int
    __hash: str

    def __init__(self, content: str | bytes):
        self.__content = content
        self.__length = len(content)
        self.__hash = self.__calculate_hash()

    def __calculate_hash(self) -> str:
        """
        Calculate the hash of the blob.

        Returns
        -------
        str
            The hash of the blob.
        """
        return hashlib.sha1(f"blob {self.__length}\0{self.__content}".encode()).hexdigest()

    @property
    def content(self) -> str | bytes:
        return self.__content

    @content.setter
    def content(self, content: str | bytes):
        self.__content = content
        self.__length = len(content)
        self.__hash = self.__calculate_hash()

    @property
    def length(self) -> int:
        return self.__length

    @property
    def hash(self) -> str:
        return self.__hash

    def __str__(self) -> str:
        return f"Blob: {self.__hash}"

    def __repr__(self) -> str:
        return f"Blob: {self.__hash}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Blob):
            return NotImplemented
        return self.__hash == other.hash