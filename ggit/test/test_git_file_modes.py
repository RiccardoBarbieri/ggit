from genericpath import isfile
from pprint import pprint
import subprocess
import shutil
import os
from pathlib import Path
from typing import Dict, List

def octal_to_string(octal):
    result = ""
    conv = {
        '0': '---',
        '1': '--x',
        '2': '-w-',
        '3': '-wx',
        '4': 'r--',
        '5': 'r-x',
        '6': 'rw-',
        '7': 'rwx',
    }
    # Iterate over each of the digits in octal
    num = str(oct(octal))[2:]
    num = num.zfill(3)
    if len(num) > 3:
        raise ValueError("Invalid permission number")
    for digit in num:
        result += conv[str(digit)]
    return result

modes_folder = Path(__file__).parent.joinpath('modes')
if not modes_folder.exists():
    os.mkdir(modes_folder)
os.chdir(modes_folder)

# create a file for each unix mode
for i in range(0, 8*8*8):
    mode = oct(i)
    
    if not Path(modes_folder.joinpath(mode)).exists():
        with open(modes_folder.joinpath(mode), 'w+') as f:
            f.write(mode)
    
    os.chmod(modes_folder.joinpath(mode), i)

for i in range(0, 8*8*8):
    mode = oct(i)

    if not Path(modes_folder.joinpath('d' + mode)).exists():
        os.mkdir(modes_folder.joinpath('d' + mode))
        with open(modes_folder.joinpath('d' + mode, 'placeholder'), 'w+') as f:
            f.write(mode)

subprocess.run(['git', 'init'], stdout=subprocess.PIPE)

faulty_files = []
for i in os.listdir(modes_folder):
    if os.path.isfile(modes_folder.joinpath(i)):
        add_process = subprocess.run(['git', 'add', i], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if add_process.stderr:
            faulty_files.append(i)
faulty_folders = []
for i in os.listdir(modes_folder):
    if os.path.isdir(modes_folder.joinpath(i)):
        add_process = subprocess.run(['git', 'add', i], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if add_process.stderr:
            faulty_folders.append(i)

if not modes_folder.joinpath('link').exists():
    os.symlink(modes_folder.joinpath('0o777'), modes_folder.joinpath('link'))
subprocess.run(['git', 'add', 'link'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


subprocess.run(['git', 'commit', '-m', 'test'], stdout=subprocess.PIPE)

print(len(faulty_files)) 
# if user does not have read permission on file, git will not add it
# for i in faulty_files:
#     print(octal_to_string(int(i, 8)))
print(len(faulty_folders))

log_process = subprocess.run(['git', 'cat-file', '-p', 'HEAD'], stdout=subprocess.PIPE)
tree_hash = log_process.stdout.decode('utf-8').split(' ')[1].split('\n')[0].strip()
tree_process = subprocess.run(['git', 'cat-file', '-p', tree_hash], stdout=subprocess.PIPE)

modes: Dict[str, List[str]] = {}
for i in tree_process.stdout.decode('utf-8').splitlines():
    git_mode = i.split(' ')[0]
    file_name = i.split(' ')[-1].split('\t')[-1]
    try:
        modes[git_mode].append(file_name)
    except KeyError:
        modes[git_mode] = [file_name]
print('All git modes:')
pprint(modes.keys())


os.remove(modes_folder.joinpath('link'))
for i in os.listdir(modes_folder):
    if os.path.isfile(modes_folder.joinpath(i)):
        os.remove(modes_folder.joinpath(i))
    else:
        shutil.rmtree(modes_folder.joinpath(i))
