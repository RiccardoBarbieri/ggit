import os
from pathlib import Path
from pprint import pprint as print
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.database import BlobRepository
from ggit.utils.nodes_utils import parse_tree
from ggit.entities import Blob, Tree
from neo4j import Result


class TreeRepository:
    """
    This repository class implements methods to add, get and delete trees from the database.
    It uses the DataSource class to create a session with the database and execute queries.

    Attributes
    ----------
    data_source: :class:`ggit.database.DataSource`
        The data source used to create a session with the database.
    """

    data_source: "DataSource"

    def __init__(self, data_source: "DataSource") -> None:
        self.data_source = data_source

    def add_tree(self, tree: Tree) -> Tuple[bool, int]:
        """
        This method adds a tree to the database, managing all the nodes and relationships
        that are part of the tree. It uses an instance of the :class:`ggit.database.BlobRepository`
        class to add the blobs to the database.

        Parameters
        ----------
        tree: :class:`ggit.entities.Tree`
            The tree to be added to the database.

        Returns
        -------
        Tuple[bool, int]
            A tuple containing a boolean value that indicates if the tree was added successfully
            and the number of nodes created, useful information given that the method is used
            recursively.
        """
        nodes_created = 0
        with self.data_source.new_session() as session:
            try:
                tx = session.begin_transaction()

                # if tree already exists return false
                result = tx.run(
                    "MATCH (tree:Tree {hash: $hash}) RETURN tree", hash=tree.hash
                )
                if result.single() is not None:
                    return (False, nodes_created)

                tx.run(
                    "MERGE (t:Tree {hash: $hash, content: $content, length: $length}) RETURN t",
                    hash=tree.hash,
                    content=tree.content,
                    length=tree.length,
                )
                nodes_created += 1

                blob_repo = BlobRepository(self.data_source)

                for item in tree.items:
                    if isinstance(item[0], Tree):
                        result = self.add_tree(item[0])
                        tx.run(
                            "MATCH (t:Tree {hash: $hash}) MATCH (t2:Tree {hash: $hash2}) MERGE (t)-[:INCLUDES {mode: $mode, name: $name}]->(t2)",
                            hash=tree.hash,
                            hash2=item[0].hash,
                            name=item[1],
                            mode=item[2],
                        )
                        nodes_created += result[1]
                    else:
                        blob_repo.add_blob(item[0])
                        nodes_created += 1
                        tx.run(
                            "MATCH (t:Tree {hash: $tree_hash}), (b:Blob {hash: $blob_hash}) MERGE (t)-[:INCLUDES {mode: $mode, name: $name}]->(b)",
                            tree_hash=tree.hash,
                            blob_hash=item[0].hash,
                            name=item[1],
                            mode=item[2],
                        )

                tx.commit()
            except Exception as e:
                tx.rollback()
                raise e
            return (nodes_created == tree.item_count, nodes_created)

    def get_tree(self, hash: str) -> Tree:
        """
        This method gets a tree from the database given its hash.
        It makes use of the :func:`ggit.utils.nodes_utils.parse_tree` function to parse the tree
        given the nodes obtained from the database and the hash of the top tree in the relations.

        Parameters
        ----------
        hash: str
            The hash of the tree to be retrieved.

        Returns
        -------
        :class:`ggit.entities.Tree`
            The tree retrieved from the database.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH relation = (tree:Tree {hash: $hash})-[:INCLUDES*1..]->(item) RETURN tree, relation, item",
                hash=hash,
            )

            return parse_tree(hash, result.graph().nodes, result.graph().relationships)

    def get_all_trees(self) -> List[Tree]:
        """
        This method gets all the trees from the database.

        Returns
        -------
        List[:class:`ggit.entities.Tree`]
            A list containing all the trees in the database.
        """
        with self.data_source.new_session() as session:
            result: Result = session.run("MATCH (tree:Tree) RETURN tree")
            return [self.get_tree(record["tree"]["hash"]) for record in result]

    def delete_tree(self, hash: str) -> bool:
        """
        This method deletes a tree from the database given its hash.
        All relationships and nodes that are related to the tree are deleted.

        Parameters
        ----------
        hash: str
            The hash of the tree to be deleted.

        Returns
        -------
        bool
            A boolean value that indicates if the tree was deleted successfully.
        """
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH (tree:Tree {hash: $hash})-[r*1..]->(n) DETACH DELETE tree, n", hash=hash
            )
            return result.consume().counters.nodes_deleted >= 1


def load_trees():
    main_tree = Tree()
    for i in os.listdir(
        Path(__file__).parent.parent / "test" / "assets" / "tree_tester"
    ):
        path = Path(__file__).parent.parent / "test" / "assets" / "tree_tester" / i
        if path.is_file():
            with open(path, "rb") as f:
                main_tree.append_item(
                    Blob(f.read()), i, "100644" if path.name != "bin" else "100755"
                )
        if path.is_dir():
            sub_tree = Tree()
            for j in os.listdir(path):
                sub_path = path / j
                if sub_path.is_file():
                    with open(sub_path, "rb") as f:
                        sub_tree.append_item(Blob(f.read()), j, "100644")
    main_tree.append_item(sub_tree, "sub", "040000")
    return main_tree


if __name__ == "__main__":
    from ggit.database import DataSource

    data = DataSource()
    tree_repo = TreeRepository(data)

    main_tree = load_trees()

    tree_repo.add_tree(main_tree)

    data.close()
