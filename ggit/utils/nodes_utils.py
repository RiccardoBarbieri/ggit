from typing import List

from ggit.entities import Blob, Tree
from neo4j.graph import Node, Relationship


def get_node(hash: str, nodes: List[Node]) -> Node:
    for node in nodes:
        if node['hash'] == hash:
            return node
    return None

def parse_tree(hash: str, nodes: List[Node], relations: List[Relationship]) -> Tree:
    tree_node: Node = get_node(hash, nodes)
    tree = Tree()
    sub_nodes: List[Relationship] = [i for i in relations if i.start_node == tree_node]
    for i in sub_nodes:
        if 'Blob' in i.end_node.labels:
            tree.append_item(Blob(i.end_node['content']), i['name'], i['mode'])
        elif 'Tree' in i.end_node.labels:
            tree.append_item(parse_tree(i.end_node['hash'], nodes, relations), i['name'], i['mode'])
    return tree