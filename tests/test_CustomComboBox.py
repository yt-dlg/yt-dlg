#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Contains test cases for the widgets.py module."""


import sys
import os.path
import unittest
from unittest import mock

PATH = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(PATH)))

try:
    import wx

    from youtube_dl_gui.widgets import CustomComboBox
except ImportError as error:
    print(error)
    sys.exit(1)


class TestCustomComboBox(unittest.TestCase):
    """Test cases for the CustomComboBox widget."""

    def setUp(self):
        self.app = wx.App()

        self.frame = wx.Frame(None)
        self.combobox = CustomComboBox(self.frame)

        # Call directly the ListBoxWithHeaders methods
        self.combobox.listbox.GetControl().add_header("Header")
        self.combobox.listbox.GetControl().add_items(["item%s" % i for i in range(10)])

    def tearDown(self):
        self.frame.Destroy()
        del self.app

    def test_init(self):
        combobox = CustomComboBox(
            self.frame, -1, "item1", choices=["item0", "item1", "item2"]
        )

        self.assertEqual(combobox.GetValue(), "item1")
        self.assertEqual(combobox.GetCount(), 3)
        self.assertEqual(combobox.GetSelection(), 1)

    # wx.ComboBox methods
    # Not all of them since most of them are calls to ListBoxWithHeaders
    # methods and we already have tests for those

    def test_is_list_empty_false(self):
        self.assertFalse(self.combobox.IsListEmpty())

    def test_is_list_empty_true(self):
        self.combobox.Clear()
        self.assertTrue(self.combobox.IsListEmpty())

    def test_is_text_empty_false(self):
        self.combobox.SetValue("somevalue")
        self.assertFalse(self.combobox.IsTextEmpty())

    def test_is_text_empty_true(self):
        self.assertTrue(self.combobox.IsTextEmpty())

    def test_set_selection_item(self):
        self.combobox.SetSelection(1)
        self.assertEqual(self.combobox.GetSelection(), 1)
        self.assertEqual(self.combobox.GetValue(), "item0")

    def test_set_selection_header(self):
        self.combobox.SetSelection(0)
        self.assertEqual(self.combobox.GetSelection(), wx.NOT_FOUND)
        self.assertEqual(self.combobox.GetValue(), "")

    def test_set_string_selection_item(self):
        self.combobox.SetStringSelection("item0")
        self.assertEqual(self.combobox.GetStringSelection(), "item0")
        self.assertEqual(self.combobox.GetValue(), "item0")

    def test_set_string_selection_header(self):
        self.combobox.SetStringSelection("Header")
        self.assertEqual(self.combobox.GetStringSelection(), "")
        self.assertEqual(self.combobox.GetValue(), "")

    def test_set_string_selection_invalid_string(self):
        self.combobox.SetStringSelection("abcde")
        self.assertEqual(self.combobox.GetStringSelection(), "")
        self.assertEqual(self.combobox.GetValue(), "")

    # wx.ItemContainer methods

    def test_clear(self):
        self.combobox.SetValue("value")

        self.combobox.Clear()
        self.assertEqual(self.combobox.GetCount(), 0)
        self.assertTrue(self.combobox.IsTextEmpty())

    def test_append(self):
        self.combobox.Append("item10")
        self.assertEqual(self.combobox.GetCount(), 12)

    def test_append_items(self):
        self.combobox.AppendItems(["item10", "item11"])
        self.assertEqual(self.combobox.GetCount(), 13)

    def test_delete(self):
        self.combobox.Delete(1)
        self.assertEqual(self.combobox.GetString(1), "item1")

    # wx.TextEntry methods

    def test_get_value(self):
        self.combobox.SetValue("value")
        self.assertEqual(self.combobox.GetValue(), "value")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
