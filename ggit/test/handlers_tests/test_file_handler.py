import os
import unittest
from pathlib import Path

from ggit.handlers.file_handler import add_handler, mv_handler, paths_parser, rm_handler
from ggit.handlers.init_handler import init_repository
from ggit.managers import StashManager


class TestFileHandlers(unittest.TestCase):

    REPO_ROOT = Path("/home/riccardoob/thesis/ggit/test/assets/tree_tester")

    def setUp(self) -> None:
        init_repository(self.REPO_ROOT)
        return super().setUp()

    def test_0_add(self):
        paths = [
            "filetest.txt",
            "sub/asd.t",
        ]
        add_handler(paths)
        stash_manager = StashManager(self.REPO_ROOT)
        self.assertTrue(len(stash_manager.stashed_files) == 2)
        self.assertTrue(len(stash_manager.tracked_files) == 2)

        parsed_paths = paths_parser(paths, self.REPO_ROOT)

        for i in parsed_paths:
            self.assertTrue(str(i) in stash_manager.stashed_files)
            self.assertTrue(str(i) in stash_manager.tracked_files)

    def test_1_mv(self):
        source = "filetest.txt"
        dest = "sub/filetest.txt"

        parsed_source = paths_parser([source], self.REPO_ROOT)[0]
        parsed_dest = self.REPO_ROOT / Path(dest)
        stash_manager = StashManager(self.REPO_ROOT)

        mv_handler(source, dest)

        self.assertTrue(len(stash_manager.stashed_files) == 2)
        self.assertTrue(len(stash_manager.tracked_files) == 2)

        self.assertTrue(str(parsed_source) not in stash_manager.stashed_files)
        self.assertTrue(str(parsed_source) not in stash_manager.tracked_files)
        self.assertTrue(str(parsed_dest) in stash_manager.stashed_files)
        self.assertTrue(str(parsed_dest) in stash_manager.tracked_files)

        mv_handler(dest, source)

        self.assertTrue(str(parsed_source) in stash_manager.stashed_files)
        self.assertTrue(str(parsed_source) in stash_manager.tracked_files)
        self.assertTrue(str(parsed_dest) not in stash_manager.stashed_files)
        self.assertTrue(str(parsed_dest) not in stash_manager.tracked_files)

    def test_2_rm(self):
        paths = [
            "filetest.txt",
            "sub/asd.t",
        ]
        with open(self.REPO_ROOT / "filetest.txt", "r") as f:
            filetest_txt = f.read()
        with open(self.REPO_ROOT / "sub" / "asd.t", "r") as f:
            asd_t = f.read()

        rm_handler(paths)
        stash_manager = StashManager(self.REPO_ROOT)
        self.assertTrue(len(stash_manager.stashed_files) == 0)
        self.assertTrue(len(stash_manager.tracked_files) == 0)

        with open(self.REPO_ROOT / "filetest.txt", "w+") as f:
            f.write(filetest_txt)
        with open(self.REPO_ROOT / "sub" / "asd.t", "w+") as f:
            f.write(asd_t)

    def tearDown(self) -> None:
        open(self.REPO_ROOT / ".ggit" / "stash.json", "w+").close()
        open(self.REPO_ROOT / ".ggit" / "tracked_files.json", "w+").close()
        return super().tearDown()


if __name__ == "__main__":
    os.chdir("/home/riccardoob/thesis/ggit/test/assets/tree_tester")
    unittest.main()
