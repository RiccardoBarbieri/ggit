import logging
from logging import Logger
import os
from pathlib import Path
from typing import List

from ggit.managers import ConfigManager, StashManager, config_manager
from ggit.utils.folder_utils import is_subpath
from ggit.exceptions import RepositoryException


def paths_parser(
    arguments: List[str], root: Path, logger: Logger = logging.getLogger("message")
) -> List[Path]:
    paths: List[Path] = []
    for i in arguments:
        paths.append(Path(i).resolve())
        if not paths[-1].exists():
            logger.error(f"Path {paths[-1]} does not match any file or directory")
            raise RepositoryException(f"Path {paths[-1]} does not match any file or directory")
        if not is_subpath(paths[-1], root):
            logger.error(f"Path {paths[-1]} is not in the repository")
            raise RepositoryException(f"Path {paths[-1]} is not in the repository")
    return paths


def add(arguments: List[str], logger: Logger = logging.getLogger("message")) -> None:
    
    config_manager = ConfigManager()
    root = Path(config_manager["repository.path"]).resolve()
    stash_manager = StashManager(root)

    paths = paths_parser(arguments, root, logger)

    logger.debug("Stashing files...")
    for i in paths:
        logger.debug(f"Stashing {i}")
        stash_manager.stash(i)
    logger.debug("Stashing completed")


def rm_handler(arguments: List[str], logger: Logger = logging.getLogger("message")) -> None:

    config_manager = ConfigManager()
    root = Path(config_manager["repository.path"]).resolve()
    stash_manager = StashManager(root)

    paths = paths_parser(arguments, root, logger)

    logger.debug("Removing files...")
    for i in paths:
        logger.debug(f"Removing {i}")
        stash_manager.unstash(i)
    logger.debug("Removing completed")


def mv_handler(source: str, dest: str, logger: Logger = logging.getLogger("message")) -> None:

    config_manager = ConfigManager()
    root = Path(config_manager["repository.path"]).resolve()
    stash_manager = StashManager(root)

    source = paths_parser([source], root, logger)[0]
    if not is_subpath(dest, root):
        logger.error(f"Path {dest} is not in the repository")
        exit(1)
    dest = Path(dest).resolve()


    logger.debug("Moving files...")
    stash_manager.move(source, dest)
    logger.debug("Moving completed")
