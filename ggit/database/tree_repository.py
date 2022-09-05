import os
from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple
from pprint import pprint as print

if TYPE_CHECKING:
    from ggit.database import DataSource

from ggit.database import BlobRepository
from ggit.entities import Blob, Tree
from neo4j import Record, Result, Transaction


class TreeRepository:

    data_source: 'DataSource'

    def __init__(self, data_source: 'DataSource') -> None:
        self.data_source = data_source

    def add_tree(self, tree: Tree) -> Tuple[bool, int]:
        nodes_created = 0
        with self.data_source.new_session() as session:
            tx = session.begin_transaction()
            
            # if tree already exists return false
            result = tx.run("MATCH (tree:Tree {hash: $hash}) RETURN tree", hash=tree.hash)
            if result.single() is not None:
                return (False, nodes_created)

            tx.run("CREATE (t:Tree {hash: $hash, content: $content, length: $length}) RETURN t",
                            hash=tree.hash, content=tree.content, length=tree.length)
            nodes_created += 1
            
            blob_repo = BlobRepository(self.data_source)

            for item in tree.items:
                if isinstance(item[0], Tree):
                    result = self.add_tree(item[0])
                    tx.run("MATCH (t:Tree {hash: $hash}) MATCH (t2:Tree {hash: $hash2}) CREATE (t)-[:INCLUDES {mode: $mode, name: $name}]->(t2)",
                           hash=tree.hash, hash2=item[0].hash, name=item[1], mode=item[2])
                    nodes_created += result[1]
                else:
                    blob_repo.add_blob(item[0])
                    nodes_created += 1
                    tx.run("MATCH (t:Tree {hash: $tree_hash}), (b:Blob {hash: $blob_hash}) CREATE (t)-[:INCLUDES {mode: $mode, name: $name}]->(b)",
                        tree_hash=tree.hash, blob_hash=item[0].hash, name=item[1], mode=item[2])

            tx.commit()
            return (nodes_created == tree.item_count, nodes_created)

    def get_tree(self, hash: str) -> Tree:
        with self.data_source.new_session() as session:
            result = session.run(
                "MATCH (tree:Tree {hash: $hash})-[:INCLUDES*1..]->(item) RETURN tree, item", hash=hash)
            
            print(result.data())
            
            return result.data()


def load_trees():
    main_tree = Tree()
    for i in os.listdir(Path(__file__).parent.parent /  'test' / 'assets' / 'tree_tester'):
        path = Path(__file__).parent.parent /  'test' / 'assets' / 'tree_tester' / i
        if path.is_file():
            with open(path, 'rb') as f:
                main_tree.append_item(Blob(f.read()), i, '100644' if path.name != 'bin' else '100755')
        if path.is_dir():
            sub_tree = Tree()
            for j in os.listdir(path):
                sub_path = path / j
                if sub_path.is_file():
                    with open(sub_path, 'rb') as f:
                        sub_tree.append_item(Blob(f.read()), j, '100644')
    main_tree.append_item(sub_tree, 'sub', '040000')
    return main_tree

if __name__ == '__main__':
    from ggit.database import DataSource

    data = DataSource()
    a = TreeRepository(data)

    main_tree = load_trees()

    a.get_tree(main_tree.hash)
    

    data.close()
