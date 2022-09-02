import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from time import sleep

from ggit.entities import Blob, Commit, Tree, User
from ggit.utils import walk_folder_flat
from rich.console import Console

repo = Path(__file__).parent.joinpath('assets', 'tree_tester')

shutil.rmtree(repo)
os.mkdir(repo)
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

date_time = datetime.now()

log_process = subprocess.run(['git', 'log', '--pretty=format:%H', '-n', '1'], stdout=subprocess.PIPE)
real_hash = log_process.stdout.decode('utf-8').strip()

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

commit = Commit()

commit.tree = main_tree
commit.parent = None
commit.date_time = date_time
commit.author = User('RiccardoBarbieri', 'riccardo_barbieri@outlook.it')
commit.committer = User('RiccardoBarbieri', 'riccardo_barbieri@outlook.it')
commit.message = 'test'

console = Console()
console.print(f"[blue]main_tree[/blue]")
if commit.hash == real_hash:
    console.print(f"[green]{real_hash} -> {commit.hash}[/green]")
else:
    console.print(f"[red]{real_hash} -> {commit.hash}[/red]")
assert commit.hash == real_hash
