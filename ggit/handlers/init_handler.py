import json
from logging import Logger
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess

from ggit.managers import ConfigManager, DifferenceManager
from ggit.exceptions import ConfigException
from ggit.managers.neo4j_manager import start_neo4j_instance

def search_neo4j() -> Path | None:
    sub = Path('bin/neo4j.ps1') if os.name == 'nt' else Path('bin/neo4j')
    try:
        path = os.environ['NEO4J_HOME']
        if (Path(path) / sub).exists():
            process = subprocess.run([str(Path(path) / sub), 'version'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            stdout = process.stdout.decode().strip()
            if stdout.startswith('neo4j'):
                return Path(path), stdout.split(' ')[1]
    except KeyError:
        return None, None


def init_repository(path: Path, logger: Logger = logging.getLogger("message")) -> None:
    """
    Function used to initialize a new repository.
    The repository will be initialized in the directory passed as parameter.

    Parameters
    ----------
    path : Path
        Path to the directory where the repository will be initialized.
    logger : Logger
        Logger used to print messages.
    """
    logger.debug("Creating .ggit folder inside repository...")
    if (path / ".ggit").exists():
        logger.error("Repository already initialized")
        return
        
    os.makedirs(path / ".ggit", exist_ok=True)
    with open(path / ".ggit" / "tracked_files.json", "w") as f:
        json.dump([], f)
    with open(path / ".ggit" / "stash.json", "w") as f:
        json.dump({}, f)
    with open(path / ".ggit" / "config.json", "w") as f:
        json.dump({}, f)
    with open(path / ".ggit" / "current_state.json", "w") as f:
        json.dump({}, f)

    logger.debug("Storing basic configuration parameters...")
    conf_manager = ConfigManager(path)
    conf_manager["repository.path"] = str(path)
    username = input("Inserisci il tuo username: ")
    conf_manager["user.name"] = username
    while True:
        email = input("Inserisci la tua email: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        else:
            print("Email non valida, riprova")
    conf_manager["user.email"] = email
    conf_manager["HEAD"] = "None"

    logger.debug("Updating repository directory state...")
    diff_manager = DifferenceManager(path)
    diff_manager.update_current_state()

    # path_version = search_neo4j()
    # if path_version[0]:
    #     logger.debug("Neo4j found in %s", path_version[0])
    #     conf_manager["database.path"] = str(path / ".ggit" / f"neo4j-{path_version[1]}")
    #     conf_manager["database.version"] = path_version[1]
    # else:
    #     raise ConfigException("Neo4j installation not found, refer to the documentation. Did you set the NEO4J_HOME environment variable correctly?")
    # conf_manager['database.name'] = 'neo4j'
    # shutil.copytree(path_version[0], path / ".ggit" / f"neo4j-{path_version[1]}")
    # start_neo4j_instance(Path(path_version[0])) ##!inserire il path alla distro di neo4j
    # conf_manager["database.username"] = "neo4j"
    # conf_manager["database.password"] = "neo4j"

    logger.info(f"Initialized empty Ggit repository in {path / '.ggit'}")
