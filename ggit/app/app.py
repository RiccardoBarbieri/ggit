#!/home/riccardoob/thesis/venv/bin/python3

import argparse
import logging
import logging.config
import os
import re
import sys
from pathlib import Path
from typing import Any, List, Sequence

from ggit.handlers.file_handler import add_handler, mv_handler, rm_handler
from ggit.handlers.commit_handler import commit_handler
from ggit.handlers.init_handler import init_repository
from ggit.handlers.status_handler import status_handler
from ggit.utils.date_utils import date_iso_8601
from ggit.utils.folder_utils import find_repo_root


class GGitAppParser(argparse.ArgumentParser):
    """
    This class extends the argparse.ArgumentParser class to provide a custom parser for
    the GGit application.

    The class exposes a method to create all the subparsers and arguments needed to
    parse the command line arguments.

    Attributes
    ----------
    subparsers : List[argparse.ArgumentParser]
        Subparsers object used to create the subparsers.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super(GGitAppParser, self).__init__(*args, **kwargs)

    def set_up(self) -> None:
        """
        Method used to create all the subparsers and arguments parsers
        needed to parse the command line arguments.
        """
        subparsers = self.add_subparsers(
            title="Commands",
            dest="subcommand",
            description="List of available commands",
            metavar="",
        )
        self.subparsers: List[argparse.ArgumentParser] = []

        init_subparser = subparsers.add_parser(
            "init",
            help="Initialize a new repository",
            description="",
        )
        self.subparsers.append(init_subparser)

        init_subparser.add_argument(
            "path",
            nargs="?",
            default=".",
            help="The path where the repository will be created",
            metavar="<path>"
        )

        add_subparser = subparsers.add_parser(
            "add", help="Add files and directories to the index."
        )
        self.subparsers.append(add_subparser)

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
        self.subparsers.append(mv_subparser)

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
        self.subparsers.append(rm_subparser)

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
        self.subparsers.append(commit_subparser)

        commit_message_options = commit_subparser.add_argument_group()
        file_excl_group = commit_message_options.add_mutually_exclusive_group(
            required=True
        )
        file_excl_group.add_argument(
            "-f",
            "--file",
            nargs="?",
            help="Read the commit message from the given file",
            type=argparse.FileType("r"),
            metavar="file",
            dest="message_file",
        )
        file_excl_group.add_argument(
            "-m",
            "--message",
            help="The commit message",
            metavar="message",
            dest="message",
        )
        commit_message_options.add_argument(
            "--author",
            nargs="?",
            help="Override author for this commit",
            type=str,
            metavar="name,email",
            dest="author",
        )
        commit_message_options.add_argument(
            "--date",
            nargs="?",
            help="Override date for this commit, formatted as YYYY-MM-DDTHH:mm:SS+HH:mm",
            type=date_iso_8601,
            metavar="date",
            dest="date",
        )

        log_subparser = subparsers.add_parser(
            "log",
            help="Show commit logs",
        )
        self.subparsers.append(log_subparser)

        log_subparser.add_argument(
            "-d",
            "--depth",
            action="store",
            type=int,
            default=5,
            help="Limit the number of commits to output",
            metavar="<depth>",
            dest="depth",
        )

        status_subparser = subparsers.add_parser(
            "status",
            help="Show the working tree status",
        )
        self.subparsers.append(status_subparser)

        config_subparser = subparsers.add_parser(
            "config",
            help="Get and set repository options",
        )
        self.subparsers.append(config_subparser)

        config_group = config_subparser.add_mutually_exclusive_group(required=True)
        config_group.add_argument(
            "--get",
            nargs=1,
            help="Get the value of a configuration variable",
            metavar="<key>",
            dest="get",
        )
        config_group.add_argument(
            "--set",
            nargs=2,
            help="Set the value of a configuration variable",
            metavar=("<key>", "<value>"),
            dest="set",
        )
        config_group.add_argument(
            "--unset",
            nargs=1,
            help="Unset the value of a configuration variable",
            metavar="<key>",
            dest="unset",
        )
        config_group.add_argument(
            "--list",
            action="store_true",
            help="List all configuration variables",
            dest="list",
        )

        for i in self.subparsers:
            i.add_argument(
                "-v", "--verbose", action="store_true", help="Verbose output"
            )


def main() -> None:
    """
    The main function of the application.
    Inside this function, that is called in the main block of code, the command line arguments are parsed using
    the :class:`GGitAppParser` class, the logger is configured and loaded
    and the corresponding handler is called depending on the subcommand
    passed as argument.
    """

    parser = GGitAppParser(
        prog="ggit",
        description="GGit, a simple VCS base on a graph database and inspired by git.",
        allow_abbrev=False,
    )
    parser.set_up()
    
    #!_____________________________________
    # args = 'log'
    # pattern = re.compile(r'([^\s"\']+)|"([^"]*)"|(\'([^\']*)\')')

    # args = [i.group().strip('"\'') for i in pattern.finditer(args)]
    
    # sys.argv += args
    #!_____________________________________
    if len(sys.argv) == 2 and sys.argv[1] == "init":
        sys.argv.append(".")

    if len(sys.argv) == 1 or sys.argv[1] == "help":
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()
    args = vars(args)

    logging.config.fileConfig(Path(__file__).parent.parent / "utils" / "logging.conf")
    if args["verbose"]:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger("message")

    if args["subcommand"] == "init":
        init_repository(Path(args["path"]).resolve(), logger)

    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        logger.error("Not a ggit repository, (or any of the parent directories)")
        sys.exit(1)
    elif args["subcommand"] == "add":
        add_handler(args["path"], logger)
    elif args["subcommand"] == "mv":
        mv_handler(args["source"], args["destination"], logger)
    elif args["subcommand"] == "rm":
        rm_handler(args["path"], logger)
    elif args["subcommand"] == "commit":
        commit_handler(args, logger)
    elif args["subcommand"] == "log":
        pass
    elif args["subcommand"] == "status":
        status_handler(logger)
    elif args["subcommand"] == "config":
        pass


if __name__ == "__main__":
    main()
