"""Contains test cases for the ClipDialog in widgets.py module."""

import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING, cast

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))


from tests.wtc import WidgetTestCase

from youtube_dl_gui.downloadmanager import DownloadItem
from youtube_dl_gui.widgets import ClipDialog

if TYPE_CHECKING:
    from youtube_dl_gui.mainframe import MainFrame


class TestClipDialog(WidgetTestCase):
    """Test cases for the ClipDialog widget."""

    def test_get_timespans(self):
        ditem = DownloadItem("url", ["-f", "flv"])
        self.dlg = ClipDialog(cast("MainFrame", self.frame), ditem)

        # No timespans
        self.assertEqual(self.dlg._get_timespans(), ("0:00:00", "0:00:00"))

        # With timespans
        self.dlg = ClipDialog(cast("MainFrame", self.frame), ditem)

        option_timespan = ["--external-downloader-args", "-ss 70 -to 165"]
        self.dlg.download_item.options.extend(option_timespan)

        self.assertEqual(self.dlg._get_timespans(), ("0:01:10", "0:02:45"))
        self.assertEqual(len(self.dlg.download_item.options), 4)

        # self.dlg.clip_start.SetValue(wx.TimeSpan(0, 1, 10))  # "0:01:10"
        # self.dlg.clip_end.SetValue(wx.TimeSpan(0, 2, 45))  # "0:02:45"

    def test_get_timespans_no_exist(self):
        """With timespans no send (no exist)"""
        ditem = DownloadItem("url", ["-f", "flv"])
        self.dlg = ClipDialog(cast("MainFrame", self.frame), ditem)

        option_timespan = ["--external-downloader-args"]
        self.dlg.download_item.options.extend(option_timespan)

        self.assertEqual(self.dlg._get_timespans(), ("0:00:00", "0:00:00"))
        self.assertEqual(len(self.dlg.download_item.options), 2)

    def test_get_timespans_no_numbers(self):
        """With timespans like strings"""
        ditem = DownloadItem("url", ["-f", "flv"])
        self.dlg = ClipDialog(cast("MainFrame", self.frame), ditem)

        option_timespan = ["--external-downloader-args", "-ss ab -to xy"]
        self.dlg.download_item.options.extend(option_timespan)

        self.assertEqual(self.dlg._get_timespans(), ("0:00:00", "0:00:00"))
        self.assertEqual(len(self.dlg.download_item.options), 2)

    def test_clean_options(self):
        """External downloader options alway last options"""
        ditem = DownloadItem("url", ["-f", "flv"])
        options = [
            "--external-downloader",
            "ffmpeg",
            "--external-downloader-args",
            "-ss 70 -to 165",
        ]

        self.dlg = ClipDialog(cast("MainFrame", self.frame), ditem)
        self.dlg.download_item.options.extend(options)

        self.assertEqual(self.dlg.download_item.options, ["-f", "flv"] + options)

        self.dlg._clean_options()

        self.assertEqual(self.dlg.download_item.options, ["-f", "flv"])

    def test_clean_options_extra_args(self):
        """Clean options and extra args in the end"""
        ditem = DownloadItem("url", ["-f", "flv"])
        options = [
            "--external-downloader",
            "ffmpeg",
            "--external-downloader-args",
            "-ss 70 -to 165",
            "-R",
            "-keep-fragments",
            "-v",
        ]

        self.dlg = ClipDialog(cast("MainFrame", self.frame), ditem)
        self.dlg.download_item.options.extend(options)

        self.dlg._clean_options()

        self.assertEqual(
            self.dlg.download_item.options, ["-f", "flv", "-R", "-keep-fragments", "-v"]
        )


if __name__ == "__main__":
    unittest.main()
