#!/home/riccardoob/thesis/venv/bin/python3

import argparse
import logging
import logging.config
from pathlib import Path
import sys
from typing import Any, List, Sequence

from ggit.utils.date_utils import date_iso_8601

from ggit.app.file_handler import add_handler, rm_handler, mv_handler
from ggit.app.init_handler import init_repository

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
            metavar="<path>",
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
        commit_message_options.add_argument(
            "-f",
            "--file",
            nargs="?",
            help="Read the commit message from the given file",
            type=argparse.FileType("r"),
            metavar="file",
            dest="message_file",
        )
        commit_message_options.add_argument(
            "--author",
            nargs="?",
            help="Override author for this commit",
            type=str,
            metavar="author",
            dest="author",
        )
        commit_message_options.add_argument(
            "--date",
            nargs="?",
            help="Override date for this commit, formatted as 2000-06-20T00:00:00+00:00",
            type=date_iso_8601,
            metavar="date",
            dest="date",
        )
        commit_message_options.add_argument(
            "-m",
            "--message",
            help="The commit message",
            metavar="message",
            required=True,
            dest="message",
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


if __name__ == "__main__":
    parser = GGitAppParser(
        prog="ggit",
        description="GGit, a simple VCS base on a graph database and inspired by git.",
        allow_abbrev=False,
    )
    parser.set_up()

    sys.argv += "rm as qa".split()

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

    match args["subcommand"]:
        case "init":
            print(args)
            # init_repository(args["path"], logger)
        case "add":
            print(args)
            # add_handler(args["path"], logger)
        case "mv":
            print(args)
            # mv_handler(args["source"], args["destination"], logger)
        case "rm":
            print(args)
            # rm_handler(args["path"], logger)
        case "commit":
            pass
        case "log":
            pass
        case "status":
            pass
        case "config":
            pass
