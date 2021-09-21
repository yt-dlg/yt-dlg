"""Contains test cases for the logmanager.py module."""

import sys
import unittest
from pathlib import Path
from unittest import mock

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))

from youtube_dl_gui.logmanager import LogManager


class TestLogManager(unittest.TestCase):
    def setUp(self) -> None:
        self.config_path: str = str(PATH.joinpath("fixtures"))

    def test_init(self):
        log_mng = LogManager(self.config_path, True)
        self.assertEqual(
            log_mng.log_file,
            str(Path(self.config_path) / Path(LogManager.LOG_FILENAME)),
        )

    @mock.patch("youtube_dl_gui.logmanager.LogManager", autospec=True)
    def test_log(self, mock_logmanager):
        opt_mng = mock_logmanager.return_value
        opt_mng.log(data="Logging from tests")
        opt_mng.log.assert_called_once()
