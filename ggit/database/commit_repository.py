from typing import TYPE_CHECKING
import traceback

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import Commit
from ggit.database import TreeRepository


class CommitRepository:

    data_source: "DataSource"

    def __init__(self) -> None:
        self.data_source = DataSource()

    def add_commit(self, commit: Commit) -> bool:
        with self.data_source.new_session() as session:
            tx = session.begin_transaction()
            try:

                tx.run(
                    "MERGE (user:User {name: $name, email: $email})",
                    name=commit.author.name,
                    email=commit.author.email,
                )
                tx.run(
                    "MERGE (user:User {name: $name, email: $email})",
                    name=commit.committer.name,
                    email=commit.committer.email,
                )

                tx.run(
                    """MATCH (author:User {name: $author_name, email: $author_email})
                    MATCH (committer:User {name: $committer_name, email: $committer_email})
                    MERGE (commit:Commit {hash: $hash, message: $message, datetime: $datetime, content: $content, length: $length})
                    MERGE (commit)-[:AUTHORED_BY]->(author)
                    MERGE (commit)-[:COMMITTED_BY]->(committer)""",
                    author_name=commit.author.name,
                    author_email=commit.author.email,
                    committer_name=commit.committer.name,
                    committer_email=commit.committer.email,
                    hash=commit.hash,
                    message=commit.message,
                    datetime=commit.date_time,
                    content=commit.content,
                    length=commit.length,
                )

                if commit.parent is not None:
                    tx.run(
                        """MATCH (parent:Commit {hash: $parent_hash})
                        MATCH (commit:Commit {hash: $hash}) 
                        MERGE (parent)-[:PARENT]->(commit)""",
                        parent_hash=commit.parent.hash,
                        hash=commit.hash,
                    )

                tree_repo = TreeRepository()
                tree_repo.add_tree(commit.tree)

                tx.run(
                    """MATCH (commit:Commit {hash: $hash})
                    MATCH (tree:Tree {hash: $tree_hash})
                    MERGE (commit)-[:CONTAINS]->(tree)""",
                    hash=commit.hash,
                    tree_hash=commit.tree.hash,
                )

                tx.commit()
            except Exception:
                tx.rollback()
                print("The following error occurred while adding the commit:")
                print(traceback.format_exc(), end="")
                return False
