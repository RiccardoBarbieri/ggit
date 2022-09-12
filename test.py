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

from ggit.utils.folder_utils import walk_folder_rec_flat, walk_objects

# os.chdir(Path(__file__).parent.joinpath("ggit", "test", "assets", "tree_tester"))

body = b"""tree ff7ae585339f04217663bdb7f54df531c6fb8217
author RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200
committer RiccardoBarbieri <riccardo_barbieri@outlook.it> 1662040308 +0200

test
"""

# print(hashlib.sha1(b"commit " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest())

a = """Directories in use:
home:         /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10
config:       /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/conf
logs:         /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/logs
plugins:      /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/plugins
import:       /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/import
data:         /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/data
certificates: /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/certificates
licenses:     /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/licenses
run:          /home/riccardoob/thesis/.ggit/neo4j-community-4.4.10/run
Starting Neo4j.
Started neo4j (pid:11894). It is available at http://0.0.0.0:7474
There may be a short delay until the server is ready."""

pid = a.splitlines()[-2].split("(pid:")[1].split(")")[0]