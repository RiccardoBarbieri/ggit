from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import Blob
from neo4j import Result


class BlobRepository:
    """
    This repository class implements methods to add, get and delete blobs from the database.
    It uses the DataSource class to create a session with the database and execute queries.

    Attributes
    ----------
    data_source: :class:`ggit.database.DataSource`
        The DataSource object used to create a session with the database.
    
    """

    data_source: 'DataSource'

    def __init__(self, data_source: 'DataSource') -> None:
        self.data_source = data_source

    def add_blob(self, blob: Blob) -> bool:
        """
        This method adds a blob to the database, creating a node with the hash, 
        length and content properties.

        Parameters
        ----------
        blob: :class:`ggit.entities.Blob`
            The blob to be added to the database.

        Returns
        -------
        bool
            True if the blob was added successfully, False otherwise.
        """
        with self.data_source.new_session() as session:
            result = session.run("MERGE (b:Blob {hash: $hash, content: $content, length: $length}) RETURN b",
                                 hash=blob.hash, content=blob.content, length=blob.length)
            return result.consume().counters.nodes_created == 1

    def get_blob(self, hash: str) -> Blob:
        """
        This method gets a blob from the database, given its hash.

        Parameters
        ----------
        hash: str
            The hash of the blob to be retrieved.

        Returns
        -------
        :class:`ggit.entities.Blob`
            The blob retrieved from the database.
        """
        with self.data_source.new_session() as session:
            result = session.run("MATCH (blob:Blob {hash: $hash}) RETURN blob", hash=hash)
            if result.single() is None:
                return None
            return Blob(result.single()['blob']['content'])

    def get_all_blobs(self) -> List[Blob]:
        """
        This method gets all the blobs from the database.

        Returns
        -------
        List[:class:`ggit.entities.Blob`]
            The list of blobs retrieved from the database.
        """
        with self.data_source.new_session() as session:
            result: Result = session.run("MATCH (blob:Blob) RETURN blob")
            return [Blob(record['blob']['content']) for record in result]

    def delete_blob(self, hash: str) -> bool:
        """
        This method deletes a blob from the database, given its hash.
        All relationships on the found blob are detached.

        Parameters
        ----------
        hash: str
            The hash of the blob to be deleted.

        Returns
        -------
        bool
            True if the blob was deleted successfully, False otherwise.
        """
        with self.data_source.new_session() as session:
            result = session.run("MATCH (blob:Blob {hash: $hash}) DETACH DELETE blob", hash=hash)
            return result.consume().counters.nodes_deleted == 1


if __name__ == '__main__':
    from ggit.database import DataSource

    data = DataSource()
    a = BlobRepository(data)
