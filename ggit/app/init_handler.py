import os
from pathlib import Path

from ggit.managers import ConfigManager
from ggit.managers import DifferenceManager

import logging

def init_repository(path: Path) -> None:


    logging.debug("Creating .ggit folder inside repository...")
    os.makedirs(path / ".ggit", exist_ok=True)

    logging.debug("Storing basic configuration parameters...")
    conf_manager = ConfigManager(path)
    conf_manager["repository.path"] = str(path)
    conf_manager["database_username"] = "neo4j"
    conf_manager["database_password"] = "neo4j"

    logging.debug("Updating repository directory state...")
    diff_manager = DifferenceManager(path)
    diff_manager.update_current_state()

    logging.info(f"Initialized empty Ggit repository in {path / '.ggit'}")