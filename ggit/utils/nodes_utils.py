from typing import List

from ggit.entities import Blob, Tree
from neo4j.graph import Node, Relationship


def get_node(hash: str, nodes: List[Node]) -> Node:
    """
    Obtains a node from a list of nodes given its hash.
    May be used only with nodes that have a hash property.

    Parameters
    ----------
    hash : str
        The hash of the node to obtain.
    nodes : List[Node]
        The list of nodes to search in.

    Returns
    -------
    Node
        The node with the given hash.
    """
    for node in nodes:
        if node['hash'] == hash:
            return node
    return None

def parse_tree(hash: str, nodes: List[Node], relations: List[Relationship]) -> Tree:
    """
    Parses a tree given the nodes and relations obtained from a query
    created to get the tree, its relationships and its items.

    Parameters
    ----------
    hash : str
        The hash of the top tree in the relations.
    nodes : List[Node]
        The list of nodes obtained from the query.
    relations : List[Relationship]
        The list of relations obtained from the query.

    Returns
    -------
    Tree
        The tree parsed from the nodes and relations.
    """
    tree_node: Node = get_node(hash, nodes)
    tree = Tree()
    sub_nodes: List[Relationship] = [i for i in relations if i.start_node == tree_node]
    for i in sub_nodes:
        if 'Blob' in i.end_node.labels:
            tree.append_item(Blob(i.end_node['content']), i['name'], i['mode'])
        elif 'Tree' in i.end_node.labels:
            tree.append_item(parse_tree(i.end_node['hash'], nodes, relations), i['name'], i['mode'])
    return tree