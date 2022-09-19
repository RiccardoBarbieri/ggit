import traceback
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.entities import Commit


class CommitRepository:
    """
    This repository class implements methods to add, get and delete commits from the database.
    It uses the DataSource class to create a sessione with the database and execute queries.

    Attributes
    ----------
    data_source : DataSource
        The data source used to create a session with the database.
    """

    data_source: "DataSource"

    def __init__(self) -> None:
        self.data_source = DataSource()

    def add_commit(self, commit: Commit) -> bool:
        from ggit.database import TreeRepository, UserRepository
        """
        This method adds a commit to the database, managing all the nodes and relationships that are
        part of the commit. It adds the users using the UserRepository class, the tree contained in
        the commit using the TreeRepository class and the commit itself.

        Parameters
        ----------
        commit : Commit
            The commit to add to the database.

        Returns
        -------
        bool
            True if the commit was added successfully, False otherwise.
        """
        with self.data_source.new_session() as session:
            tx = session.begin_transaction()
            try:
                counters = {}

                user_repo = UserRepository()

                user_repo.add_user(commit.author)
                user_repo.add_user(commit.committer)

                result = tx.run(
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
                    datetime=commit.str_date_time,
                    content=commit.content,
                    length=commit.length,
                )

                counters["nodes_created"] = result.consume().counters.nodes_created
                counters["relationships_created"] = result.consume().counters.relationships_created

                if commit.parent is not None:
                    result = tx.run(
                        """MATCH (parent:Commit {hash: $parent_hash})
                        MATCH (commit:Commit {hash: $hash}) 
                        MERGE (parent)<-[:PARENT]-(commit)""",
                        parent_hash=commit.parent.hash,
                        hash=commit.hash,
                    )
                    counters["relationships_created"] += result.consume().counters.relationships_created

                tree_repo = TreeRepository()
                tree_correct = tree_repo.add_tree(commit.tree)[0]

                result = tx.run(
                    """MATCH (commit:Commit {hash: $hash})
                    MATCH (tree:Tree {hash: $tree_hash})
                    MERGE (commit)-[:CONTAINS]->(tree)""",
                    hash=commit.hash,
                    tree_hash=commit.tree.hash,
                )
                counters["relationships_created"] += result.consume().counters.relationships_created

                tx.commit()

            except Exception:
                tx.rollback()
                print("The following error occurred while adding the commit:")
                print(traceback.format_exc(), end="")
                return False

            return (counters["nodes_created"] == 1 and counters["relationships_created"] == 3 + (1 if commit.parent is not None else 0) and tree_correct)

    def get_commit(self, hash: str) -> Commit:
        from ggit.database import TreeRepository, UserRepository
        """
        This method gets a commit from the database given its hash.
        It makes use of the UserRepository class to get the author and committer of the commit and
        the TreeRepository class to get the tree contained in the commit.

        Parameters
        ----------
        hash : str
            The hash of the commit to get.

        Returns
        -------
        Commit
            The commit with the given hash.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                """MATCH (commit:Commit {hash: $hash})-->[:CONTAINS]-(tree:Tree)
                RETURN commit, tree""",
                hash=hash,
            )
            record = result.single()
            if record is None:
                return None

            tree = TreeRepository().get_tree(record["tree"]["hash"])
            
            result = session.run(
                """MATCH (commit:Commit {hash: $hash})-[:AUTHORED_BY]->(author:User)
                RETURN author""",
                hash=hash,
            )
            record = result.single()
            author = UserRepository().get_user(record["author"]["name"], record["author"]["email"])

            result = session.run(
                """MATCH (commit:Commit {hash: $hash})-[:COMMITTED_BY]->(committer:User)
                RETURN committer""",
                hash=hash,
            )
            record = result.single()
            committer = UserRepository().get_user(record["committer"]["name"], record["committer"]["email"])

            result = session.run(
                """MATCH (commit:Commit {hash: $hash})-[:PARENT]->(parent:Commit)
                RETURN parent""",
                hash=hash,
            )
            record = result.single()
            if record is None:
                parent = None
            else:
                parent = self.get_commit(record["parent"]["hash"])

            commit = Commit(
                tree=tree,
                parent=parent,
                # date_time=record["commit"]["datetime"],
                author=author,
                committer=committer,
                message=record["commit"]["message"],
            )
            commit.str_date_time = record["commit"]["datetime"]

            return commit

    def get_all_commits(self) -> List[Commit]:
        """
        This method gets all the commits from the database.

        Returns
        -------
        List[Commit]
            A list of all the commits in the database.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                """MATCH (commit:Commit)
                RETURN commit""",
            )
            return [self.get_commit(record["commit"]["hash"]) for record in result]
    
    def delete_commit(self, hash: str) -> bool:
        """
        This method deletes a commit from the database given its hash, and all the relationships
        that it has with other nodes.
        The tree contained in the commit is not deleted, as it may be contained in other commits,
        mereover, the author and committer of the commit are not deleted, as they may have authored
        or committed other commits.

        Parameters
        ----------
        hash : str
            The hash of the commit to delete.

        Returns
        -------
        bool
            True if the commit was deleted, False otherwise.
        """
        with self.data_source.new_session() as session:
            tx = session.begin_transaction()
            try:
                result = tx.run(
                    """MATCH (commit:Commit {hash: $hash})
                    DETACH DELETE commit""",
                    hash=hash,
                )
                tx.commit()
            except Exception:
                tx.rollback()
                print("The following error occurred while deleting the commit:")
                print(traceback.format_exc(), end="")
                return False

            return result.consume().counters.nodes_deleted == 1