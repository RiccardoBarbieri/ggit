import logging
from logging import Logger
from pathlib import Path
from typing import Dict

from ggit.database.commit_repository import CommitRepository
from ggit.managers.config_manager import ConfigManager

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_handler(args: Dict[str, str], logger: Logger = logging.getLogger("message")) -> None:
    """This handler"""

    root = Path(ConfigManager()["repository.path"])

    number = int(args["depth"])

    if number == 0:
        return

    head = ConfigManager()["HEAD"]
    if head is None or head == "" or head == "None":
        print("No commits yet")
        return

    commit_repository = CommitRepository()
    last_commits = commit_repository.get_last_commits(head, number)

    for commit in last_commits:
        print(f"\033[93mcommit {commit.hash}\033[0m \033[96m(HEAD)\033[0m")
        print(f"Author: {commit.author}")
        print(f'Date: {commit.date_time.strftime("%a %b %d %H:%M:%S %Y %z")}')
        print()
        print(f"    {commit.message}")
        print()
