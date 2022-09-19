import logging
import logging.config
import mimetypes
import os
import subprocess
import sys
from pathlib import Path
import hashlib
from datetime import datetime, timedelta, timezone
import traceback
from typing import Any, NewType
import typing

from ggit.utils.folder_utils import walk_folder_rec_flat, walk_objects

# os.chdir(Path(__file__).parent.joinpath("ggit", "test", "assets", "tree_tester"))

body = b"""tree ff7ae585339f04217663bdb7f54df531c6fb8217
author RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200
committer RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200

test
"""

# print(hashlib.sha1(b"commit " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest())
def isNewType(obj: Any) -> bool:
    """Check the if object is a kind of NewType."""
    if sys.version_info >= (3, 10):
        return isinstance(obj, typing.NewType)
    else:
        __module__ = safe_getattr(obj, '__module__', None)
        __qualname__ = safe_getattr(obj, '__qualname__', None)
        if __module__ == 'typing' and __qualname__ == 'NewType.<locals>.new_type':
            return True
        else:
            return False

print(isNewType(body))