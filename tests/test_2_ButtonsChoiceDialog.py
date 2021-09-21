"""Contains test cases for the ButtonsChoiceDialog in widgets.py module."""

import sys
import unittest
from pathlib import Path

PATH = Path(__file__).parent
sys.path.insert(0, str(PATH.parent))


from tests.wtc import WidgetTestCase

from youtube_dl_gui.widgets import ButtonsChoiceDialog


class TestButtonsChoiceDialog(WidgetTestCase):
    """Test cases for the ButtonsChoiceDialog widget."""

    def test_init_dark(self):
        _dark_mode = True
        choices = ["Remove all", "Remove completed"]
        btn_choice_dlg = ButtonsChoiceDialog(
            self.frame, choices, "Test ButtonsChoiceDialog", "Test", _dark_mode
        )
        self.assertTrue(btn_choice_dlg._dark_mode)
        self.assertEqual(len(btn_choice_dlg.buttons), 3)


if __name__ == "__main__":
    unittest.main()
