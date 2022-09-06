from ggit.database import DataSource
from ggit.entities import Commit


class CommitRepository:

    data_source: "DataSource"

    def __init__(self) -> None:
        self.data_source = DataSource()

    def add_commit(self, commit: Commit) -> bool:
        with self.data_source.new_session() as session:
            result = session.run(
                "MERGE (c:Commit {hash: $hash, author: $author, date: $date, message: $message}) RETURN c",
                hash=commit.hash,
                author=commit.author,
                date=commit.date,
                message=commit.message,
            )
            return result.consume().counters.nodes_created == 1
