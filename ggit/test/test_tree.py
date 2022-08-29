from ast import main
import sys
from pathlib import Path

from rich.console import Console

sys.path.append(Path(__file__).parent.parent.parent.__str__())

from ggit.converter.git_connector import GitConnectorSubprocess
from ggit.entities import Blob, Tree
from ggit.utils import walk_folder_flat

main_tree = Tree()

sub_tree = Tree()
with open(Path(__file__).parent.parent.parent.joinpath('git_test').joinpath('folder').joinpath("asd.txt"), 'rb') as f:
    blob1 = Blob(f.read())
    sub_tree.append_item(blob1, "asd.txt", "100644")

main_tree.append_item(sub_tree, "folder", "040000")

with open(Path(__file__).parent.parent.parent.joinpath('git_test').joinpath("asd2.txt"), 'rb') as f:
    blob2 = Blob(f.read())
    main_tree.append_item(blob2, "asd2.txt", "100644")

print("100644 blob " + blob2.hash + "\t" + "asd2.txt")
print("040000 tree " + sub_tree.hash + "\t" + "folder")
print(main_tree.hash)