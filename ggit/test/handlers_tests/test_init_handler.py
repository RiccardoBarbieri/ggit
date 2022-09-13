import os
import shutil
import unittest
from pathlib import Path

from genericpath import isfile
from ggit.handlers.init_handler import init_repository
from ggit.managers import ConfigManager, DifferenceManager, StashManager


class TestFileHandlers(unittest.TestCase):

    REPO_ROOT = Path("/home/riccardoob/thesis/ggit/test/assets/tree_tester")

    def setUp(self) -> None:
        shutil.rmtree(self.REPO_ROOT / ".ggit")
        return super().setUp()

    def test_0_init(self):
        init_repository(self.REPO_ROOT)
        self.assertTrue(Path(self.REPO_ROOT) / ".ggit")
        self.assertTrue(Path(self.REPO_ROOT) / ".ggit" / "tracked_files.json")
        self.assertTrue(Path(self.REPO_ROOT) / ".ggit" / "stash.json")
        self.assertTrue(Path(self.REPO_ROOT) / ".ggit" / "config.json")
        self.assertTrue(Path(self.REPO_ROOT) / ".ggit" / "current_state.json")

        diff_manager = DifferenceManager(self.REPO_ROOT)
        config_manager = ConfigManager(self.REPO_ROOT)

        for i in self.REPO_ROOT.iterdir():
            if i.is_file():
                self.assertTrue(str(i) in diff_manager.files)

        self.assertEqual(config_manager["repository.path"], str(self.REPO_ROOT))
        self.assertEqual(config_manager["database_username"], "neo4j")
        self.assertEqual(config_manager["database_password"], "neo4j")


if __name__ == "__main__":
    unittest.main()
