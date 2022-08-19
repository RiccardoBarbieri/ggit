import os
from pathlib import Path
from typing import List


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
