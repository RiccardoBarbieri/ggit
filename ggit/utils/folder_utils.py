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

# def walk_folder_flat(folder: Path, get: str = 'files') -> List[Path]:
#     """
#     Walk a folder and by default returns all files found.
#     If get is set to 'folders' it will return all folders found, and
#     if get is set to 'both' it will return both files and folders.
#     The files are returned as a list of Path objects.

#     Parameters
#     ----------
#     folder: Path
#         The folder to walk.
#     get: str, optional
#         The type of files to return. Can be 'files', 'folders' or 'both'.

#     Returns
#     -------
#     List[Path]
#         The list of Path objects of the files found.
#     """
#     if get not in ['files', 'folders', 'both']:
#         raise ValueError("get must be 'files', 'folders' or 'both'")
#     files = []
#     walk = os.walk(folder)
#     if get == 'files':
#         for i in walk:
#             if i[2]:
#                 for j in i[2]:
#                     files.append(Path.joinpath(Path(i[0]), j))
#     elif get == 'folders':
#         for i in walk:
#             if i[1]:
#                 for j in i[1]:
#                     files.append(Path.joinpath(Path(i[0]), j))
#     elif get == 'both':
#         for i in walk:
#             if i[2]:
#                 for j in i[2]:
#                     files.append(Path.joinpath(Path(i[0]), j))
#             if i[1]:
#                 for j in i[1]:
#                     files.append(Path.joinpath(Path(i[0]), j))
#     return files

def walk_folder_flat(folder: Path) -> List[Path]:
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
    files = []
    walk = os.walk(folder)
    for i in walk:
        if i[2]:
            for j in i[2]:
                files.append(Path.joinpath(Path(i[0]), j))
    return files