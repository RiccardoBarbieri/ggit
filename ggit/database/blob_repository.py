from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import Blob


class BlobRepository:

    data_source: 'DataSource'

    def __init__(self, data_source: 'DataSource') -> None:
        self.data_source = data_source

    def add_blob(self, blob: Blob) -> bool:
        pass

    def get_blob(self, sha1: str) -> Blob:
        pass

    def get_all_blobs(self) -> List[Blob]:
        pass

    def delete_blob(self, sha1: str) -> bool:
        pass

    def update_blob(self, blob: Blob) -> bool:
        pass
