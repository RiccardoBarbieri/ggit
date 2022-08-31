import subprocess
import sys
import os
from pathlib import Path

from ggit.utils import walk_folder_rec_flat
import mimetypes

file1 = Path(__file__).parent.joinpath('ggit', 'test', 'assets', 'tree_tester', 'sub', 'asd.t')
file2 = Path(__file__).parent.joinpath('ggit', 'test', 'assets', 'tree_tester', 'bin')

print(file1)
print(file2)

print(os.access(file1, os.X_OK))
print(os.access(file2, os.X_OK))