import logging
import logging.config
import mimetypes
import os
from pprint import pprint
import subprocess
import sys
from pathlib import Path
import hashlib
from datetime import datetime, timedelta, timezone
import traceback

from ggit.utils.folder_utils import walk_folder_rec_flat, walk_objects

# os.chdir(Path(__file__).parent.joinpath("ggit", "test", "assets", "tree_tester"))

body = b"""tree ff7ae585339f04217663bdb7f54df531c6fb8217
author RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200
committer RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200

test
"""

# print(hashlib.sha1(b"commit " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest())

from ggit.entities import Commit, Tree, Blob
from ggit.managers import StashManager

root = Path("./ggit/test/assets/tree_tester").resolve()
a = StashManager(root)

for i in walk_folder_rec_flat(root):
    if (root / i).is_file():
        a.stash(root / i)

temp = a.tracked_files
temp.sort()
pprint(temp)