"""Contains test cases for the MessageDialog in widgets.py module."""


import sys
import unittest
from pathlib import Path

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))


from tests.wtc import WidgetTestCase

from youtube_dl_gui.widgets import MessageDialog


class TestMessageDialog(WidgetTestCase):
    """Test cases for the MessageDialog widget."""

    def test_init_dark(self):
        _dark_mode = True
        msg_dlg = MessageDialog(self.frame, "Test MessageDialog", "Test", _dark_mode)
        self.assertTrue(msg_dlg._dark_mode)
        self.assertEqual(len(msg_dlg.buttons), 2)


if __name__ == "__main__":
    unittest.main()
