from pathlib import Path
import subprocess

from ggit.exceptions import RepositoryException


def start_neo4j_instance(path: Path):
    """
    This is a utility function to start an instance of the neo4j database
    server, which is used by the ggit application to store the repository
    commits and changes.

    When the server is started, the pid of the process will be stored in
    a file called "neo4j.pid" inside the .ggit folder of the repository.

    It is highly recommended to leave all configuration settings to their
    default values, but if you really know what you are doing, you can
    change them in the "neo4j.conf" file inside the neo4j-community-version
    folder inside the .ggit folder of the repository.

    By default, the neo4j server will be started on the port 7687 accessible
    with the bolt protocol at bolt://localhost:7687, and
    the web interface will be available at http://localhost:7474.

    Parameters
    ----------
    path : Path
        The path to the base folder of the repository.
    """

    #! add check server already running
    process = subprocess.run(
        ["./neo4j", "start"],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        raise RepositoryException(
            f"Neo4j server could not be started. Error message:\n{process.stderr.decode()}"
        )

    pid = process.stdout.decode().splitlines()[-2].split("(pid:")[1].split(")")[0]
    with open(path / ".ggit" / "neo4j.pid", "w+") as f:
        f.write(pid)
