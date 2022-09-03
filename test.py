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
main_content = zlib.compress(body)
sub_content = zlib.compress(body[15:50])

print(sub_content)
print(main_content)