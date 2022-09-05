from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import Blob
from neo4j import Query, Record, Result


class BlobRepository:

    data_source: 'DataSource'

    def __init__(self, data_source: 'DataSource') -> None:
        self.data_source = data_source

    def add_blob(self, blob: Blob) -> bool:
        with self.data_source.new_session() as session:
            result = session.run(
                "CREATE (b:Blob {hash: $hash, content: $content, length: $length}) RETURN b", hash=blob.hash, content=blob.content, length=blob.length)
            return result.consume().counters.nodes_created == 1

    def get_blob(self, hash: str) -> Blob:
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH (blob:Blob {hash: $hash}) RETURN blob", hash=hash)
            if result.single() is None:
                return None
            return Blob(result.single()['blob']['content'])

    def get_all_blobs(self) -> List[Blob]:
        with self.data_source.new_session() as session:
            result: Result = session.run("MATCH (blob:Blob) RETURN blob")
            return [Blob(record['blob']['content']) for record in result]

    def delete_blob(self, hash: str) -> bool:
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH (blob:Blob {hash: $hash}) DELETE blob", hash=hash)
            return result.consume().counters.nodes_deleted == 1

if __name__ == '__main__':
    from ggit.database import DataSource

    data = DataSource()
    a = BlobRepository(data)




    
