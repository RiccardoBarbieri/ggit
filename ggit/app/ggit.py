#!/home/riccardoob/thesis

import argparse


parser = argparse.ArgumentParser(
    prog = "ggit",
    description = "GGit, a simple VCS base on a graph database and inspired by git.",
    allow_abbrev=False
)

parser.add_argument(
    "add",
    help = "Add file contents to the index",
    nargs = "+",
    metavar = "PATH"
)


