#!/usr/bin/env python

"""Contains test cases for the downloadmanager.py module."""


import sys
import unittest
from pathlib import Path
from unittest import mock

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))

from youtube_dl_gui.downloadmanager import DownloadItem, DownloadList, DownloadManager


class TestDownloadManager(unittest.TestCase):
    @mock.patch("youtube_dl_gui.downloadmanager.DownloadManager", autospec=True)
    def test_init_check_sig(self, mock_dwlmng):
        dwn_manager = mock_dwlmng(parent=None, download_list=[], opt_manager=None)
        dwn_manager._running = True
        self.assertIsInstance(dwn_manager, DownloadManager)
        self.assertTrue(dwn_manager._running)

    @mock.patch("youtube_dl_gui.downloadmanager.Worker")
    @mock.patch("youtube_dl_gui.mainframe.MainFrame")
    @mock.patch("youtube_dl_gui.optionsmanager.OptionsManager")
    def test_downloadmanager(self, mock_opt_manager, mock_mainframe, mock_worker):
        config_path = "/home/user/.config"
        dwl_list = DownloadList(
            [
                DownloadItem("url1", ["-v", "-F"]),
                DownloadItem("url2", ["-v", "-F"]),
                DownloadItem("url3", ["-v", "-F"]),
            ]
        )
        opt_manager = mock_opt_manager(config_path)
        opt_manager.options = {
            "youtubedl_path": config_path,
            "workers_number": 3,
            "disable_update": True,
        }
        parent = mock_mainframe(opt_manager)
        mock_worker.available.return_value = True
        # End thread for this test like daemon
        # TODO: Finished join the thread
        dwn_manager = DownloadManager(parent, dwl_list, opt_manager, daemon=True)

        self.assertTrue(dwn_manager._running)
        self.assertEqual(dwn_manager.name, "DownloadManager")
        self.assertEqual(len(dwn_manager._workers), 3)
        dwn_manager.stop_downloads()
        self.assertFalse(dwn_manager._running)
        self.assertTrue(dwn_manager._jobs_done())


def main():
    unittest.main()


if __name__ == "__main__":
    main()
