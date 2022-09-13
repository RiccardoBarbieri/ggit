import os
import subprocess
import shutil
from pathlib import Path

from ggit.git_utils.model.hash_type import HashType
from ggit.git_utils.git_connector import GitConnectorSubprocess
from ggit.entities import Blob, Tree
from ggit.utils.folder_utils import walk_folder_flat
from rich.console import Console

repo = Path(__file__).parent.joinpath('assets', 'tree_tester')

process = subprocess.run(['rm', '-rf', repo])
process = subprocess.run(['mkdir', repo])
os.chdir(repo)

os.mkdir('sub')
with open('sub/asd.t', 'w+') as f:
    f.write('asdacas')
with open('filetest.txt', 'w+') as f:
    f.write('testo importante da hashare')
with open('new_file.txt', 'w+') as f:
    f.write('asdavcasc')
shutil.copy(repo.parent.parent.parent.parent.joinpath('get_objects'), 'bin')

subprocess.run(['git', 'init'], stdout=subprocess.PIPE)
subprocess.run(['git', 'add', '.'], stdout=subprocess.PIPE)
subprocess.run(['git', 'commit', '-m', 'test'], stdout=subprocess.PIPE)

connector = GitConnectorSubprocess()

# getting tree hashes from test repository
trees = [obj for obj in connector.get_all_objects() if obj[1] == HashType.TREE]

# identifying the trees
cat_process = subprocess.run(['git', 'cat-file', '-p', trees[0][0]], stdout=subprocess.PIPE)
main_tree = None
sub_tree = None
if 'sub' in cat_process.stdout.decode('utf-8'):
    main_tree_hash_real = trees[0][0]
    sub_tree_hash_real = trees[1][0]
else:
    main_tree_hash_real = trees[1][0]
    sub_tree_hash_real = trees[0][0]

items_sub = []
for i in walk_folder_flat(repo.joinpath('sub')):
    if os.access(i, os.X_OK):
        mode = '100755'
    elif i.is_symlink():
        mode = '120000'
    else:
        mode = '100644'
    items_sub.append((Blob(i.read_bytes()), i.name, mode))

sub_tree = Tree(items_sub)
items_main = []
for i in walk_folder_flat(repo):
    if os.access(i, os.X_OK):
        mode = '100755'
    elif i.is_symlink():
        mode = '120000'
    else:
        mode = '100644'
    items_main.append((Blob(i.read_bytes()), i.name, mode))
items_main.append((sub_tree, 'sub', '040000'))
main_tree = Tree(items_main)

# comparing the trees
console = Console()
console.print(f"[blue]main_tree[/blue]")
if main_tree.hash == main_tree_hash_real:
    console.print(f"[green]{main_tree_hash_real} -> {main_tree.hash}[/green]")
else:
    console.print(f"[red]{main_tree_hash_real} -> {main_tree.hash}[/red]")
assert main_tree.hash == main_tree_hash_real

console.print(f"[blue]sub_tree[/blue]")
if sub_tree.hash == sub_tree_hash_real:
    console.print(f"[green]{sub_tree_hash_real} -> {sub_tree.hash}[/green]")
else:
    console.print(f"[red]{sub_tree_hash_real} -> {sub_tree.hash}[/red]")
assert sub_tree.hash == sub_tree_hash_real


# subprocess.run(['rm', '-rf', '.git'])
