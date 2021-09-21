"""Contains test cases for the optionsmanager.py module."""

import sys
import unittest
from pathlib import Path
from unittest import mock

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))

from youtube_dl_gui.optionsmanager import OptionsManager


class TestOptionsManager(unittest.TestCase):
    def setUp(self) -> None:
        self.config_path: str = str(PATH.joinpath("fixtures"))

    def test_init(self):
        opt_mng = OptionsManager(self.config_path)
        self.assertEqual(
            opt_mng.settings_file,
            str(Path(self.config_path) / Path(OptionsManager.SETTINGS_FILENAME)),
        )

    @mock.patch("youtube_dl_gui.optionsmanager.OptionsManager", autospec=True)
    def test_save_to_file(self, mock_optionsmanager):
        opt_mng = mock_optionsmanager.return_value
        opt_mng.save_to_file()
        opt_mng.save_to_file.assert_called_once()


def main():
    unittest.main()


if __name__ == "__main__":
    main()
