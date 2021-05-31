# -*- coding: UTF-8 -*-

"""Custom widgets for yt-dlg"""


import os
from typing import Callable, Dict, List, Optional, Set

import wx

from .darktheme import DARK_BACKGROUND_COLOUR, DARK_FOREGROUND_COLOUR

_: Callable[[str], str] = wx.GetTranslation


def crt_command_event(event: wx.PyEventBinder, event_id: int = 0) -> wx.CommandEvent:
    """Shortcut to create command events."""
    return wx.CommandEvent(event.typeId, event_id)


# noinspection PyUnresolvedReferences
class ListBoxWithHeaders(wx.ListBox):
    """Custom ListBox object that supports 'headers'.

    Attributes:
        NAME (str): Default name for the name argument of the __init__.

        TEXT_PREFIX (str): Text to add before normal items in order to
            distinguish them (normal items) from headers.

        EVENTS (list): List with events to overwrite to avoid header selection.

    """

    NAME = "listBoxWithHeaders"

    TEXT_PREFIX = "    "

    EVENTS: List[wx.PyEventBinder] = [
        wx.EVT_LEFT_DOWN,
        wx.EVT_LEFT_DCLICK,
        wx.EVT_RIGHT_DOWN,
        wx.EVT_RIGHT_DCLICK,
        wx.EVT_MIDDLE_DOWN,
        wx.EVT_MIDDLE_DCLICK,
    ]

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        choices=[],
        style=0,
        validator=wx.DefaultValidator,
        name=NAME,
    ) -> None:
        super(ListBoxWithHeaders, self).__init__(
            parent, id, pos, size, choices, style, validator, name
        )
        self.__headers: Set[str] = set()

        # Ignore all key events i'm bored to handle the header selection
        self.Bind(wx.EVT_KEY_DOWN, lambda event: None)

        # Make sure that a header is never selected
        self.Bind(wx.EVT_LISTBOX, self._on_listbox)
        for _event in self.EVENTS:
            self.Bind(_event, self._disable_header_selection)

        # Append the items in our own way in order to add the TEXT_PREFIX
        self.AppendItems(choices)

    def _disable_header_selection(self, event) -> None:
        """Stop event propagation if the selected item is a header."""
        row = self.HitTest(event.GetPosition())
        event_skip = True

        if row != wx.NOT_FOUND and self.GetString(row) in self.__headers:
            event_skip = False

        event.Skip(event_skip)

    def _on_listbox(self, event) -> None:
        """Make sure no header is selected."""
        if event.GetString() in self.__headers:
            self.Deselect(event.GetSelection())
        event.Skip()

    def _add_prefix(self, string: str) -> str:
        return self.TEXT_PREFIX + string

    def _remove_prefix(self, string: str) -> str:
        if string[: len(self.TEXT_PREFIX)] == self.TEXT_PREFIX:
            return string[len(self.TEXT_PREFIX) :]
        return string

    # wx.ListBox methods

    def FindString(self, string: str, **kwargs) -> int:
        index = super(ListBoxWithHeaders, self).FindString(string, **kwargs)

        if index == wx.NOT_FOUND:
            # This time try with prefix
            index = super(ListBoxWithHeaders, self).FindString(
                self._add_prefix(string), **kwargs
            )

        return index

    def GetStringSelection(self) -> str:
        return self._remove_prefix(super(ListBoxWithHeaders, self).GetStringSelection())

    def GetString(self, index: int) -> str:
        if index < 0 or index >= self.GetCount():
            # Return empty string based on the wx.ListBox docs
            # for some reason parent GetString does not handle
            # invalid indices
            return ""

        return self._remove_prefix(super(ListBoxWithHeaders, self).GetString(index))

    def InsertItems(self, items: List[str], pos: int) -> None:
        items = [self._add_prefix(item) for item in items]
        super(ListBoxWithHeaders, self).InsertItems(items, pos)

    def SetSelection(self, index: int) -> None:
        if self.GetString(index) in self.__headers:
            self.Deselect(self.GetSelection())
        else:
            super(ListBoxWithHeaders, self).SetSelection(index)

    def SetString(self, index: int, string: str) -> None:
        old_string = self.GetString(index)

        if old_string in self.__headers and string != old_string:
            self.__headers.remove(old_string)
            self.__headers.add(string)

        super(ListBoxWithHeaders, self).SetString(index, string)

    def SetStringSelection(self, string: str) -> bool:
        if string in self.__headers:
            return False

        self.SetSelection(
            self.FindString(
                string,
            )
        )
        return True

    # wx.ItemContainer methods

    def AppendItems(self, strings: List[str], with_prefix: bool = True) -> None:
        if with_prefix:
            strings = [self._add_prefix(string) for string in strings]

        super(ListBoxWithHeaders, self).AppendItems(strings)

    def Clear(self) -> None:
        self.__headers.clear()
        super(ListBoxWithHeaders, self).Clear()

    def Delete(self, index: int) -> None:
        string: str = self.GetString(index)

        if string in self.__headers:
            self.__headers.remove(string)

        super(ListBoxWithHeaders, self).Delete(index)

    # Extra methods

    def add_header(self, header_string: str) -> int:
        self.__headers.add(header_string)
        return super(ListBoxWithHeaders, self).Append(header_string)

    def add_item(
        self,
        item: str,
        with_prefix: bool = True,
        clientData: Optional[Dict[str, str]] = None,
    ) -> None:
        if with_prefix:
            item = self._add_prefix(item)

        super(ListBoxWithHeaders, self).Append(item, clientData)

    def add_items(self, items: List[str], with_prefix: bool = True) -> None:
        for item in items:
            self.add_item(item, with_prefix)


# noinspection PyUnresolvedReferences
class ListBoxComboPopup(wx.ComboPopup):
    """ListBoxWithHeaders as a popup"""

    def __init__(
        self, parent: Optional[wx.ComboCtrl] = None, darkmode: bool = False
    ) -> None:
        super(ListBoxComboPopup, self).__init__()
        self.__parent = parent
        self.__listbox: Optional[ListBoxWithHeaders] = None
        self.__dark_mode: bool = darkmode

    def _on_motion(self, event) -> None:
        row: int = self.__listbox.HitTest(event.GetPosition())

        if row != wx.NOT_FOUND:
            self.__listbox.SetSelection(row)

            self.curitem = row if self.__listbox.IsSelected(row) else wx.NOT_FOUND

    # noinspection PyUnusedLocal
    def _on_left_down(self, event) -> None:
        self.value = self.curitem
        if self.value >= 0:
            self.Dismiss()

    # wx.ComboPopup methods

    # noinspection PyAttributeOutsideInit
    def Init(self) -> None:
        self.value = self.curitem = -1

    def Create(self, parent: wx.ComboCtrl, **kwargs) -> bool:
        # Create components
        self.__listbox = ListBoxWithHeaders(parent, style=wx.LB_SINGLE)

        if self.__dark_mode:
            self.__listbox.SetBackgroundColour(DARK_BACKGROUND_COLOUR)
            self.__listbox.SetForegroundColour(DARK_FOREGROUND_COLOUR)

        self.__listbox.Bind(wx.EVT_MOTION, self._on_motion)
        self.__listbox.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)

        return True

    def GetControl(self) -> Optional[ListBoxWithHeaders]:
        return self.__listbox

    def AddItem(
        self,
        item: str,
        with_prefix: bool = True,
        clientData: Optional[Dict[str, str]] = None,
    ) -> None:
        self.__listbox.add_item(item, with_prefix, clientData)

    def AddItems(self, items: List[str], with_prefix: bool = True) -> None:
        self.__listbox.add_items(items, with_prefix)

    def GetStringValue(self) -> str:
        return self.__listbox.GetString(self.value)

    def GetSelection(self) -> int:
        return self.value

    def SetSelection(self, index: int) -> None:
        self.__listbox.SetSelection(index)

        if self.__listbox.IsSelected(index):
            self.value = index
            self.__parent.SetValue(self.GetStringValue())

    def SetStringSelection(self, string: str) -> None:
        index: int = self.__listbox.FindString(
            string,
        )
        self.__listbox.SetSelection(index)

        if index != wx.NOT_FOUND and self.__listbox.GetSelection() == index:
            self.value = index
            self.SetSelection(self.value)

    def Clear(self) -> None:
        self.__parent.SetValue("")
        self.__listbox.Clear()

    def IsListEmpty(self) -> bool:
        return self.__listbox.GetCount() == 0

    def OnDismiss(self) -> None:
        if self.value < 0:
            self.value = 0
            self.__listbox.SetSelection(self.value)


# noinspection PyPep8Naming
class ExtComboBox(wx.ComboBox):
    def __init__(self, parent, max_items=-1, *args, **kwargs):
        super(ExtComboBox, self).__init__(parent, *args, **kwargs)

        assert max_items > 0 or max_items == -1
        self.max_items = max_items

    def Append(self, new_value):
        if self.FindString(new_value) == wx.NOT_FOUND:
            super(ExtComboBox, self).Append(new_value)

            if self.max_items != -1 and self.GetCount() > self.max_items:
                self.SetItems(self.GetStrings()[1:])

    def SetValue(self, new_value):
        index = self.FindString(new_value)

        if index == wx.NOT_FOUND:
            self.Append(new_value)

        self.SetSelection(index)

    def LoadMultiple(self, items_list):
        for item in items_list:
            self.Append(item)


class DoubleStageButton(wx.Button):
    def __init__(self, parent, labels, bitmaps, bitmap_pos=wx.TOP, *args, **kwargs):
        super(DoubleStageButton, self).__init__(parent, *args, **kwargs)

        assert isinstance(labels, tuple) and isinstance(bitmaps, tuple)
        assert len(labels) == 2
        assert len(bitmaps) == 0 or len(bitmaps) == 2

        self.labels = labels
        self.bitmaps = bitmaps
        self.bitmap_pos = bitmap_pos

        self._stage = 0
        self._set_layout()

    def _set_layout(self):
        self.SetLabel(self.labels[self._stage])

        if len(self.bitmaps):
            self.SetBitmap(self.bitmaps[self._stage], self.bitmap_pos)

    def change_stage(self):
        self._stage = 0 if self._stage else 1
        self._set_layout()

    def set_stage(self, new_stage):
        assert new_stage == 0 or new_stage == 1

        self._stage = new_stage
        self._set_layout()


class ButtonsChoiceDialog(wx.Dialog):

    if os.name == "nt":
        STYLE = wx.DEFAULT_DIALOG_STYLE
    else:
        STYLE = wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX

    BORDER = 10

    def __init__(self, parent, choices, message, *args, **kwargs):
        super(ButtonsChoiceDialog, self).__init__(
            parent, wx.ID_ANY, *args, style=self.STYLE, **kwargs
        )

        buttons = []

        # Create components
        panel = wx.Panel(self)

        info_bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MESSAGE_BOX)

        info_icon = wx.StaticBitmap(panel, wx.ID_ANY, info_bmp)
        msg_text = wx.StaticText(panel, wx.ID_ANY, message)

        buttons.append(wx.Button(panel, wx.ID_CANCEL, _("Cancel")))

        for index, label in enumerate(choices):
            buttons.append(wx.Button(panel, index + 1, label))

        # Get the maximum button width & height
        max_width = max_height = -1

        for button in buttons:
            button_width, button_height = button.GetSize()

            if button_width > max_width:
                max_width = button_width

            if button_height > max_height:
                max_height = button_height

        max_width += 10

        # Set buttons width & bind events
        for button in buttons:
            if button != buttons[0]:
                button.SetMinSize((max_width, max_height))
            else:
                # On Close button change only the height
                button.SetMinSize((-1, max_height))

            button.Bind(wx.EVT_BUTTON, self._on_close)

        # Set sizers
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        message_sizer = wx.BoxSizer(wx.HORIZONTAL)
        message_sizer.Add(info_icon)
        message_sizer.AddSpacer(10)
        message_sizer.Add(msg_text, flag=wx.EXPAND)

        vertical_sizer.Add(message_sizer, 1, wx.ALL, border=self.BORDER)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for button in buttons[1:]:
            buttons_sizer.Add(button)
            buttons_sizer.AddSpacer(5)

        buttons_sizer.AddSpacer(1)
        buttons_sizer.Add(buttons[0])
        vertical_sizer.Add(buttons_sizer, flag=wx.EXPAND | wx.ALL, border=self.BORDER)

        panel.SetSizer(vertical_sizer)

        width, height = panel.GetBestSize()
        self.SetSize((width, height * 1.3))

        self.Center()

    def _on_close(self, event):
        self.EndModal(event.GetEventObject().GetId())


class ShutdownDialog(wx.Dialog):

    if os.name == "nt":
        STYLE = wx.DEFAULT_DIALOG_STYLE
    else:
        STYLE = wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX

    TIMER_INTERVAL = 1000  # milliseconds

    BORDER = 10

    def __init__(self, parent, timeout, message, *args, **kwargs):
        super(ShutdownDialog, self).__init__(
            parent, wx.ID_ANY, *args, style=self.STYLE, **kwargs
        )
        assert timeout > 0

        self.timeout = timeout
        self.message = message

        # Create components
        panel = wx.Panel(self)

        info_bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MESSAGE_BOX)
        info_icon = wx.StaticBitmap(panel, wx.ID_ANY, info_bmp)

        self.msg_text = msg_text = wx.StaticText(panel, wx.ID_ANY, self._get_message())
        ok_button = wx.Button(panel, wx.ID_OK, _("OK"))
        cancel_button = wx.Button(panel, wx.ID_CANCEL, _("Cancel"))

        # Set layout
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        message_sizer = wx.BoxSizer(wx.HORIZONTAL)
        message_sizer.Add(info_icon)
        message_sizer.AddSpacer((10, 10))
        message_sizer.Add(msg_text, flag=wx.EXPAND)

        vertical_sizer.Add(message_sizer, 1, wx.ALL, border=self.BORDER)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(ok_button)
        buttons_sizer.AddSpacer((5, -1))
        buttons_sizer.Add(cancel_button)

        vertical_sizer.Add(
            buttons_sizer, flag=wx.ALIGN_RIGHT | wx.ALL, border=self.BORDER
        )

        panel.SetSizer(vertical_sizer)

        width, height = panel.GetBestSize()
        self.SetSize((width * 1.3, height * 1.3))

        self.Center()

        # Set up timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)
        self.timer.Start(self.TIMER_INTERVAL)

    def _get_message(self):
        return self.message.format(self.timeout)

    # noinspection PyUnusedLocal
    def _on_timer(self, event):
        self.timeout -= 1
        self.msg_text.SetLabel(self._get_message())

        if self.timeout <= 0:
            self.EndModal(wx.ID_OK)

    def Destroy(self):
        self.timer.Stop()
        return super(ShutdownDialog, self).Destroy()


class ButtonsGroup:

    WIDTH = 0
    HEIGHT = 1

    def __init__(self, buttons_list=[], squared=False):
        self._buttons_list = buttons_list
        self._squared = squared

    def set_size(self, size):
        assert len(size) == 2

        width, height = size

        if width == -1:
            for button in self._buttons_list:
                cur_width = button.GetSize()[self.WIDTH]

                if cur_width > width:
                    width = cur_width

        if height == -1:
            for button in self._buttons_list:
                cur_height = button.GetSize()[self.HEIGHT]

                if cur_height > height:
                    height = cur_height

        if self._squared:
            width = height = width if width > height else height

        for button in self._buttons_list:
            button.SetMinSize((width, height))

    def create_sizer(self, orient=wx.HORIZONTAL, space=-1):
        box_sizer = wx.BoxSizer(orient)

        for button in self._buttons_list:
            box_sizer.Add(button)

            if space != -1:
                box_sizer.AddSpacer((space, space))

        return box_sizer

    def bind_event(self, event, event_handler):
        for button in self._buttons_list:
            button.Bind(event, event_handler)

    def disable_all(self):
        for button in self._buttons_list:
            button.Enable(False)

    def enable_all(self):
        for button in self._buttons_list:
            button.Enable(True)

    def add(self, button):
        self._buttons_list.append(button)
