import logging
from logging import Logger
from pathlib import Path
from typing import List

from ggit.managers import ConfigManager, StashManager, config_manager
from ggit.exceptions import RepositoryException
from ggit.utils.folder_utils import is_subpath


def paths_parser(
    arguments: List[str], root: Path, logger: Logger = logging.getLogger("message")
) -> List[Path]:
    """
    This function provides a way to test if a list of strings, interpreted as paths, are valid.
    A valid path is a path that is inside the repository and that exists.

    Parameters
    ----------
    arguments : List[str]
        List of paths to test.
    root : Path
        Path to the repository root.
    logger : Logger
        Logger used to print messages.

    Returns
    -------
    List[Path]
        List of valid paths.

    Raises
    ------
    RepositoryException
        If a path is not valid.
    """
    paths: List[Path] = []
    for i in arguments:
        paths.append((root / Path(i)).resolve())
        if not paths[-1].exists():
            logger.error(f"Path {paths[-1]} does not match any file or directory")
            raise RepositoryException(f"Path {paths[-1]} does not match any file or directory")
        if not is_subpath(paths[-1], root):
            logger.error(f"Path {paths[-1]} is not in the repository")
            raise RepositoryException(f"Path {paths[-1]} is not in the repository")
    return paths


def add_handler(arguments: List[str], logger: Logger = logging.getLogger("message")) -> None:
    """
    This handler is used to add files to the repository stashing area.
    The files that are stashed are the ones that are ready for commit and that will be 
    considered tracked by the repository.

    Parameters
    ----------
    arguments : List[str]
        List of paths to add.
    logger : Logger
        Logger used to print messages.

    Raises
    ------
    RepositoryException
        If a path is not valid.
    """
    config_manager = ConfigManager()
    root = Path(config_manager["repository.path"]).resolve()
    stash_manager = StashManager(root)

    paths = paths_parser(arguments, Path.cwd(), logger)

    logger.debug("Stashing files...")
    for i in paths:
        logger.debug(f"Stashing {i}")
        stash_manager.stash(i)
    logger.debug("Stashing completed")


def rm_handler(arguments: List[str], logger: Logger = logging.getLogger("message")) -> None:
    """
    This handler is used to remove files from the repository stashing area.
    The files that are removed will be eliminated both from the repository and from the
    file system, they will be considered untracked by the repository.

    Parameters
    ----------
    arguments : List[str]
        List of paths to remove.
    logger : Logger
        Logger used to print messages.

    Raises
    ------
    RepositoryException
        If a path is not valid.
    """
    config_manager = ConfigManager()
    root = Path(config_manager["repository.path"]).resolve()
    stash_manager = StashManager(root)

    paths = paths_parser(arguments, Path.cwd(), logger)

    logger.debug("Removing files...")
    for i in paths:
        logger.debug(f"Removing {i}")
        stash_manager.unstash(i)
    logger.debug("Removing completed")


def mv_handler(source: str, dest: str, logger: Logger = logging.getLogger("message")) -> None:
    """
    This handler is used to move files and directories in the repository stashing area.
    The files or directories that are moved will be moved in the file system and in the
    repository tracking system.

    Parameters
    ----------
    source : str
        Path to the file or directory to move.
    dest : str
        Path to the destination of the file or directory.
    logger : Logger
        Logger used to print messages.

    Raises
    ------
    RepositoryException
        If a path is not valid.
    """
    config_manager = ConfigManager()
    root = Path(config_manager["repository.path"]).resolve()
    stash_manager = StashManager(root)

    source = paths_parser([source], Path.cwd(), logger)[0]
    dest: Path = Path(dest).resolve()
    
    if not is_subpath(root, dest):
        logger.error(f"Path {dest} is not in the repository")
        exit(1)
    dest = Path(dest).resolve()


    logger.debug("Moving files...")
    stash_manager.move(source, dest)
    logger.debug("Moving completed")
