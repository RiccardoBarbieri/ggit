from genericpath import isfile
import subprocess
import shutil
import os
from pathlib import Path

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
print(len(faulty_folders))


# for i in os.listdir(modes_folder):
#     if os.path.isfile(modes_folder.joinpath(i)):
#         os.remove(modes_folder.joinpath(i))
#     else:
#         shutil.rmtree(modes_folder.joinpath(i))

