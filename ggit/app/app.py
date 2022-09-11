#!/home/riccardoob/thesis/venv/bin/python3

import argparse
import logging
import logging.config
from pathlib import Path
from typing import List

from ggit.utils.date_utils import date_iso_8601

main_parser = argparse.ArgumentParser(
    prog="ggit",
    description="GGit, a simple VCS base on a graph database and inspired by git.",
    allow_abbrev=False,
)

subparsers = main_parser.add_subparsers(
    title="Commands",
    dest="subcommand",
    description="List of available commands",
    metavar="",
)
subparsers_list: List[argparse.ArgumentParser] = []

init_subparser = subparsers.add_parser(
    "init",
    help="Initialize a new repository",
    description="",
)
subparsers_list.append(init_subparser)

init_subparser.add_argument(
    "path",
    nargs="?",
    default=".",
    help="The path where the repository will be created",
    metavar="<path>",
)

add_subparser = subparsers.add_parser(
    "add", help="Add files and directories to the index."
)
subparsers_list.append(add_subparser)

add_subparser.add_argument(
    "path",
    action="extend",
    nargs="+",
    help="The files and directories to add.",
    metavar="<path>",
)

mv_subparser = subparsers.add_parser(
    "mv", help="Move or rename a file, a directory, or a symlink."
)
subparsers_list.append(mv_subparser)

mv_subparser.add_argument(
    "source",
    help="The file, directory, or symlink to move or rename.",
    action="store",
    nargs=1,
    metavar="<source>",
)
mv_subparser.add_argument(
    "destination",
    help="The new name for the file, directory, or symlink.",
    action="store",
    nargs=1,
    metavar="<destination>",
)

rm_subparser = subparsers.add_parser(
    "rm", help="Remove files from the working tree and from the index."
)
subparsers_list.append(rm_subparser)

rm_subparser.add_argument(
    "path",
    action="extend",
    nargs="+",
    help="The files and directories to remove.",
    metavar="<path>",
)

commit_subparser = subparsers.add_parser(
    "commit", help="Commit the current state of the index."
)
subparsers_list.append(commit_subparser)

commit_message_options = commit_subparser.add_argument_group()
commit_message_options.add_argument(
    "-f",
    "--file",
    nargs="?",
    help="Read the commit message from the given file",
    type=argparse.FileType("r"),
    metavar="file",
)
commit_message_options.add_argument(
    "--author",
    nargs="?",
    help="Override author for this commit",
    type=str,
    metavar="author",
)
commit_message_options.add_argument(
    "--date",
    nargs="?",
    help="Override date for this commit, formatted as 2000-06-20T00:00:00+00:00",
    type=date_iso_8601,
    metavar="date",
)
commit_message_options.add_argument(
    "-m", "--message", help="The commit message", metavar="message", required=True
)

log_subparser = subparsers.add_parser(
    "log",
    help="Show commit logs",
)
subparsers_list.append(log_subparser)

log_subparser.add_argument(
    "-d",
    "--depth",
    action="store",
    type=int,
    default=5,
    help="Limit the number of commits to output",
    metavar="<depth>",
)

status_subparsers = subparsers.add_parser(
    "status",
    help="Show the working tree status",
)
subparsers_list.append(status_subparsers)

config_subparsers = subparsers.add_parser(
    "config",
    help="Get and set repository options",
)
subparsers_list.append(config_subparsers)

for i in subparsers_list:
    i.add_argument(
        "-v", "--verbose", action="store_true", default=0, help="Verbose output"
    )

input = "log -h".split()

print(main_parser.parse_args(input))

# set logging level
logging.config.fileConfig(Path(__file__).parent.parent / "utils" / "logging.conf")

logging.getLogger()