import json
from logging import Logger
import logging
import os
from pathlib import Path
import shutil

from ggit.managers import ConfigManager, DifferenceManager
from ggit.app.neo4j_manager import start_neo4j_instance


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
    os.makedirs(path / ".ggit", exist_ok=True)

    logger.debug("Storing basic configuration parameters...")
    conf_manager = ConfigManager(path)
    conf_manager["repository.path"] = str(path)
    conf_manager["database_username"] = "neo4j"
    conf_manager["database_password"] = "neo4j"

    with open(path / ".ggit" / "tracked_files.json", "w") as f:
        json.dump({}, f)
    with open(path / ".ggit" / "stash.json", "w") as f:
        json.dump({}, f)
    with open(path / ".ggit" / "stash.json", "w") as f:
        json.dump({}, f)
    with open(path / ".ggit" / "current_state.json", "w") as f:
        json.dump({}, f)

    logger.debug("Updating repository directory state...")
    diff_manager = DifferenceManager(path)
    diff_manager.update_current_state()

    shutil.copytree(Path(__file__).parent / "neo4j-community-4.4.10", path / ".ggit" / "neo4j-community-4.4.10")
    start_neo4j_instance(path)

    logger.info(f"Initialized empty Ggit repository in {path / '.ggit'}")
