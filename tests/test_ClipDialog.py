#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Contains test cases for the ClipDialog in widgets.py module."""


import sys
import unittest
from pathlib import Path

import wx

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))


from youtube_dl_gui.app import frame
from youtube_dl_gui.downloadmanager import DownloadItem
from youtube_dl_gui.widgets import ClipDialog


class TestClipDialog(unittest.TestCase):
    """Test cases for the ClipDialog widget."""

    def setUp(self) -> None:
        self.app = wx.App()
        self.frame = frame

    def tearDown(self):
        del self.app

    def test_get_timespans(self):
        ditem = DownloadItem("url", ["-f", "flv"])
        self.dlg = ClipDialog(self.frame, ditem)

        # No timespans
        self.assertEqual(self.dlg._get_timespans(), ("0:00:00", "0:00:00"))

        # With timespans
        self.dlg = ClipDialog(self.frame, ditem)

        option_timespan = ["--external-downloader-args", "-ss 70 -to 165"]
        self.dlg.download_item.options.extend(option_timespan)

        self.assertEqual(self.dlg._get_timespans(), ("0:01:10", "0:02:45"))

        # self.dlg.clip_start.SetValue(wx.TimeSpan(0, 1, 10))  # "0:01:10"
        # self.dlg.clip_end.SetValue(wx.TimeSpan(0, 2, 45))  # "0:02:45"

    def test_clean_options(self):
        ditem = DownloadItem("url", ["-f", "flv"])
        options = [
            "--external-downloader",
            "ffmpeg",
            "--external-downloader-args",
            "-ss 70 -to 165",
        ]

        self.dlg = ClipDialog(self.frame, ditem)
        self.dlg.download_item.options.extend(options)

        self.assertEqual(self.dlg.download_item.options, ["-f", "flv"] + options)

        self.dlg._clean_options()

        self.assertEqual(self.dlg.download_item.options, ["-f", "flv"])


if __name__ == "__main__":
    unittest.main()
