"""Contains test cases for the updatemanager.py module."""

import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))

from youtube_dl_gui.updatemanager import UpdateThread
from youtube_dl_gui.utils import YOUTUBEDL_BIN

DATA_JSON = PATH.joinpath("fixtures/updatemanager_releases_latest.json").read_text(
    encoding="utf-8"
)


class TestUpdateThread(unittest.TestCase):
    @mock.patch("youtube_dl_gui.downloadmanager.UpdateThread", autospec=True)
    def test_init_check_sig(self, mock_update):
        update_thread = mock_update(opt_manager=None, quiet=False, daemon=False)
        self.assertIsInstance(update_thread, UpdateThread)

    @mock.patch("youtube_dl_gui.updatemanager.open")
    @mock.patch("youtube_dl_gui.updatemanager.check_path")
    @mock.patch("youtube_dl_gui.updatemanager.urlopen")
    @mock.patch("youtube_dl_gui.optionsmanager.OptionsManager")
    def test_downloadmanager(
        self, mock_opt_manager, mock_urlopen, mock_check_path, mock_open
    ):
        config_path = "/home/user/.config"
        opt_manager = mock_opt_manager(config_path)
        opt_manager.options = {
            "youtubedl_path": config_path,
            "cli_backend": YOUTUBEDL_BIN,
        }

        mock_urlopen.side_effect = [StringIO(DATA_JSON), StringIO("")]

        update_thread = UpdateThread(opt_manager)
        update_thread.join()

        mock_check_path.assert_called_once()
        self.assertEqual(update_thread.cli_backend, YOUTUBEDL_BIN)
        self.assertEqual(update_thread.name, "UpdateManager")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
