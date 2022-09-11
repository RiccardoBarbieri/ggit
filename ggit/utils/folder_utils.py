import os
from pathlib import Path
from typing import List
import typing

def walk_objects(repository) -> List[Path]:
    """
    Walk the repository .git/objects folder and returns all objects found.
    The objects are returned as a list of Path objects.

    Parameters
    ----------
    repository: str
        The repository to walk.

    Returns
    -------
    List[Path]
        The list of Path objects of the git objects found.
    """
    files = []
    for i in os.walk(Path.joinpath(Path(repository), '.git', 'objects')):
        if i[2]:
            for j in i[2]:
                files.append(Path.joinpath(Path(i[0]), j))
    return files

def walk_folder_rec_flat(folder: Path) -> typing.Generator[Path, None, None]:
    """
    Walk a folder and returns all files found.
    The files are returned as a list of Path objects.

    Parameters
    ----------
    folder: Path
        The folder to walk.

    Returns
    -------
    List[Path]
        The list of Path objects of the files found.
    """
    walk = os.walk(folder)
    for i in walk:
        if i[2]:
            for j in i[2]:
                yield Path.joinpath(Path(i[0]), j)

def walk_folder_flat(folder: Path) -> typing.Generator[Path, None, None]:
    """
    Walk a folder and returns all files found at the first level.
    The files are returned as a list of Path objects.

    Parameters
    ----------
    folder: Path
        The folder to walk.

    Returns
    -------
    List[Path]
        The list of Path objects of the files found.
    """
    for i in os.listdir(folder):
        if os.path.isfile(Path.joinpath(folder, i)):
            yield Path.joinpath(folder, i)

def is_subpath(path: Path, parent: Path) -> bool:
    """
    Check if a path is a subpath of another path.

    Parameters
    ----------
    path: Path
        The path to check.
    parent: Path
        The parent path.

    Returns
    -------
    bool
        True if the path is a subpath of the parent path.
    """
    return str(path.resolve()).startswith(str(parent.resolve()))