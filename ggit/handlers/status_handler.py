import logging
from logging import Logger
from pathlib import Path

from ggit.managers.config_manager import ConfigManager
from ggit.managers.difference_manager import DifferenceManager
from ggit.managers.stash_manager import StashManager
from ggit.utils.folder import Folder

def status_handler(logger: Logger = logging.getLogger("message")) -> None:
    
    root = Path(ConfigManager()["repository.path"])

    stash_manager = StashManager(root)
    difference_manager = DifferenceManager(root)

    difference_manager.update_current_state()

    if len(stash_manager.stashed_files) == 0:
        logger.info("Nothing to commit")
    else:
        logger.info("Changes to be committed:")
        for i in stash_manager.stashed_files:
            logger.info(f"\t\033[92m{i}\033[0m")

    if len(difference_manager.different_files) != 0:
        logger.info("Modified files:")
        for i in difference_manager.different_files:
            logger.info(f"\t\033[91m{i}\033[0m")

    untracked_files = [i for i in difference_manager.files if i not in stash_manager.tracked_files]

    if len(untracked_files) != 0:
        logger.info("Untracked files:")
        for i in untracked_files:
            logger.info(f"\t\033[93m{i}\033[0m")
