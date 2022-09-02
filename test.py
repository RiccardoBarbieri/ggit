import mimetypes
import os
import subprocess
import sys
from pathlib import Path
import hashlib
from datetime import datetime, timezone

from ggit.utils import walk_folder_rec_flat

os.chdir(Path(__file__).parent.joinpath('ggit', 'test', 'assets', 'tree_tester'))

body = b"""tree ff7ae585339f04217663bdb7f54df531c6fb8217
author RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200
committer RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200

test
"""

# print(hashlib.sha1(b"commit " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest())


import zlib

with open('/home/riccardoob/thesys/asdasd.txt', 'rb') as f:
    read = f.read()
    print(len(zlib.compress(read)))
    print(len(read))

with open('/home/riccardoob/thesys/.git/objects/49/8e26ea23c2f427e95af5d267256a0fe0537259', 'rb') as f:
    read = f.read()
    print(len(zlib.decompress(read)))
    print(len(read))