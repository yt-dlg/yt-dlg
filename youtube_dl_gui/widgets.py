# -*- coding: UTF-8 -*-


import sys
from typing import Set, List, Tuple, Dict, Optional

from .darktheme import DARK_BACKGROUND_COLOUR, DARK_FOREGROUND_COLOUR

import wx


def crt_command_event(event_type, event_id=0):
    """Shortcut to create command events."""
    return wx.CommandEvent(event_type.typeId, event_id)


class ListBoxWithHeaders(wx.ListBox):
    # noinspection PyUnresolvedReferences
    """Custom ListBox object that supports 'headers'.

    Attributes:
        NAME (string): Default name for the name argument of the __init__.

        TEXT_PREFIX (string): Text to add before normal items in order to
            distinguish them (normal items) from headers.

        EVENTS (list): List with events to overwrite to avoid header selection.

    """

    NAME = "listBoxWithHeaders"

    TEXT_PREFIX = "    "

    EVENTS = [
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

    def AppendItems(self, strings: List[str], with_prefix: bool = True):
        if with_prefix:
            strings = [self._add_prefix(string) for string in strings]

        super(ListBoxWithHeaders, self).AppendItems(strings)

    def Clear(self):
        self.__headers.clear()
        super(ListBoxWithHeaders, self).Clear()

    def Delete(self, index):
        string = self.GetString(index)

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


class ListBoxComboPopup(wx.ComboPopup):
    # noinspection PyUnresolvedReferences
    """ListBoxWithHeaders as a popup"""

    def __init__(self, darkmode=False) -> None:
        super(ListBoxComboPopup, self).__init__()
        self.__listbox: Optional[ListBoxWithHeaders] = None
        self.__dark_mode = darkmode

    def _on_motion(self, event) -> None:
        row: int = self.__listbox.HitTest(event.GetPosition())

        if row != wx.NOT_FOUND:
            self.__listbox.SetSelection(row)

            if self.__listbox.IsSelected(row):
                self.curitem = row
            else:
                self.curitem = wx.NOT_FOUND

    # noinspection PyUnusedLocal
    def _on_left_down(self, event) -> None:
        self.value = self.curitem
        if self.value >= 0:
            self.Dismiss()

    # wx.ComboPopup methods

    # noinspection PyAttributeOutsideInit
    def Init(self) -> None:
        self.value = self.curitem = -1

    def Create(self, parent, **kwargs) -> bool:
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
    ):
        self.__listbox.add_item(item, with_prefix, clientData)

    def AddItems(self, items: List[str], with_prefix: bool = True):
        self.__listbox.add_items(items, with_prefix)

    def GetStringValue(self):
        return self.__listbox.GetString(self.value)

    def OnDismiss(self):
        if self.value < 0:
            self.value = 0
            self.__listbox.SetSelection(self.value)


# noinspection PyPep8Naming
class ListBoxPopup(wx.PopupTransientWindow):
    # noinspection PyUnresolvedReferences
    """ListBoxWithHeaders as a popup.

    This class uses the wx.PopupTransientWindow to create the popup and the
    API is based on the wx.combo.ComboPopup class.

    Attributes:
        EVENTS_TABLE (dict): Dictionary that contains all the events
            that this class emits.

    """

    EVENTS_TABLE = {
        "EVT_COMBOBOX": crt_command_event(wx.EVT_COMBOBOX),
        "EVT_COMBOBOX_DROPDOWN": crt_command_event(wx.EVT_COMBOBOX_DROPDOWN),
        "EVT_COMBOBOX_CLOSEUP": crt_command_event(wx.EVT_COMBOBOX_CLOSEUP),
    }

    def __init__(self, parent=None, flags=wx.BORDER_NONE) -> None:
        super(ListBoxPopup, self).__init__(parent, flags)
        self.__listbox: Optional[ListBoxWithHeaders] = None

    def _on_motion(self, event) -> None:
        row = self.__listbox.HitTest(event.GetPosition())

        if row != wx.NOT_FOUND:
            self.__listbox.SetSelection(row)

            if self.__listbox.IsSelected(row):
                self.curitem = row
            else:
                self.curitem = wx.NOT_FOUND

    # noinspection PyUnusedLocal
    def _on_left_down(self, event) -> None:
        self.value = self.curitem
        if self.value >= 0:
            self.Dismiss()

    # wx.ComboPopup methods

    # noinspection PyAttributeOutsideInit
    def Init(self) -> None:
        self.value = self.curitem = -1

    def Create(self, parent, **kwargs) -> bool:
        self.__listbox = ListBoxWithHeaders(parent, style=wx.LB_SINGLE)

        self.__listbox.Bind(wx.EVT_MOTION, self._on_motion)
        self.__listbox.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)

        sizer = wx.BoxSizer()
        sizer.Add(self.__listbox, 1, wx.EXPAND)
        self.SetSizer(sizer)
        return True

    def GetAdjustedSize(
        self, min_width: int, pref_height: int, max_height: int
    ) -> wx.Size:
        width, height = self.GetBestSize()

        width = max(width, min_width)

        if pref_height != -1:
            height = pref_height * self.__listbox.GetCount() + 5

        height = min(height, max_height)

        return wx.Size(width, height)

    def GetControl(self) -> Optional[ListBoxWithHeaders]:
        return self.__listbox

    def GetStringValue(self):
        return self.__listbox.GetString(self.value)

    # def SetStringValue(self, string):
    # self.__listbox.SetStringSelection(string)


# noinspection PyPep8Naming
class CustomComboBox(wx.Panel):
    # noinspection PyUnresolvedReferences
    """Custom combobox.

    Attributes:
        CB_READONLY (long): Read-only style. The only one supported from the
            wx.ComboBox styles.

        NAME (string): Default name for the name argument of the __init__.

    """
    # NOTE wx.ComboBox does not support EVT_MOTION inside the popup
    # NOTE Tried with ComboCtrl but i was not able to draw the button

    CB_READONLY = wx.TE_READONLY

    NAME = "customComboBox"

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        value="",
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        choices=[],
        style=0,
        validator=wx.DefaultValidator,
        name=NAME,
    ):
        super(CustomComboBox, self).__init__(parent, id, pos, size, style, name)

        assert style in [self.CB_READONLY, 0]

        # Create components
        self.textctrl = wx.TextCtrl(self, wx.ID_ANY, style=style, validator=validator)
        tc_height = self.textctrl.GetSize()[1]

        self.button = wx.Button(self, wx.ID_ANY, "▾", size=(tc_height, tc_height))

        # Create the ListBoxPopup in two steps
        self.listbox = ListBoxPopup(self)
        self.listbox.Init()
        self.listbox.Create(
            self.listbox,
        )

        # Set layout
        sizer = wx.BoxSizer()
        sizer.Add(self.textctrl, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.button)
        self.SetSizer(sizer)

        # Bind events
        self.button.Bind(wx.EVT_BUTTON, self._on_button)

        for event in ListBoxPopup.EVENTS_TABLE.values():
            self.listbox.Bind(wx.PyEventBinder(event.GetEventType()), self._propagate)

        # Append items since the ListBoxPopup does not have the 'choices' arg
        self.listbox.GetControl().AppendItems(choices)
        self.SetStringSelection(value)

    def _propagate(self, event) -> None:
        if event.GetEventType() == wx.EVT_COMBOBOX.typeId:
            self.textctrl.SetValue(self.listbox.GetStringValue())

        wx.PostEvent(self, event)

    # noinspection PyUnusedLocal
    def _on_button(self, event) -> None:
        self.Popup()

    def _calc_popup_position(self) -> Tuple[int, int]:
        tc_x_axis, tc_y_axis = self.textctrl.ClientToScreen((0, 0))
        _, tc_height = self.textctrl.GetSize()

        return tc_x_axis, tc_y_axis + tc_height

    def _calc_popup_size(self) -> Tuple[int, int]:
        me_width, _ = self.GetSize()
        _, tc_height = self.textctrl.GetSize()
        _, screen_height = wx.DisplaySize()

        _, me_y_axis = self.GetScreenPosition()

        available_height = screen_height - (me_y_axis + tc_height)
        sug_width, sug_height = self.listbox.GetAdjustedSize(
            me_width, tc_height, available_height
        )

        return me_width, sug_height

    # wx.ComboBox methods

    def Dismiss(self) -> None:
        self.listbox.Dismiss()

    # noinspection PyUnusedLocal
    def FindString(self, string, caseSensitive=False) -> int:
        # TODO handle caseSensitive
        return self.listbox.GetControl().FindString(
            string,
        )

    def GetCount(self) -> int:
        return self.listbox.GetControl().GetCount()

    def GetCurrentSelection(self) -> int:
        return self.GetSelection()

    def GetInsertionPoint(self) -> int:
        return self.textctrl.GetInsertionPoint()

    def GetSelection(self) -> int:
        return self.listbox.value

    def GetTextSelection(self) -> Optional[str]:
        return self.textctrl.GetSelection()

    def GetString(self, index) -> str:
        return self.listbox.GetControl().GetString(index)

    def GetStringSelection(self) -> Optional[str]:
        return self.listbox.GetStringValue()

    def IsListEmpty(self) -> bool:
        return self.listbox.GetControl().GetCount() == 0

    def IsTextEmpty(self) -> bool:
        return not self.textctrl.GetValue()

    def Popup(self) -> None:
        self.listbox.SetPosition(self._calc_popup_position())
        self.listbox.SetSize(self._calc_popup_size())

        self.listbox.Popup()

    def SetSelection(self, index) -> None:
        self.listbox.GetControl().SetSelection(index)
        if self.listbox.GetControl().IsSelected(index):
            self.listbox.value = index
            self.textctrl.SetValue(self.listbox.GetStringValue())

    def SetString(self, index: int, string: str) -> None:
        self.listbox.GetControl().SetString(index, string)

    def SetTextSelection(self, from_: int, to_: int) -> None:
        self.textctrl.SetSelection(from_, to_)

    def SetStringSelection(self, string: str) -> None:
        index = self.listbox.GetControl().FindString(
            string,
        )
        self.listbox.GetControl().SetSelection(index)

        if index != wx.NOT_FOUND and self.listbox.GetControl().GetSelection() == index:
            self.listbox.value = index
            self.textctrl.SetValue(string)

    def SetValue(self, value: str) -> None:
        self.textctrl.SetValue(value)

    # wx.ItemContainer methods

    def Clear(self) -> None:
        self.textctrl.Clear()
        self.listbox.GetControl().Clear()

    def Append(self, item: str) -> int:
        return self.listbox.GetControl().Append(item)

    def AppendItems(self, items: List[str]) -> None:
        self.listbox.GetControl().AppendItems(items)

    def Delete(self, index: int) -> None:
        self.listbox.GetControl().Delete(index)

    # wx.TextEntry methods

    def GetValue(self) -> str:
        return self.textctrl.GetValue()

    # ListBoxWithHeaders methods

    def add_header(self, header: str) -> None:
        self.listbox.GetControl().add_header(header)

    def add_item(self, item: str, with_prefix=True) -> None:
        self.listbox.GetControl().add_item(item, with_prefix)

    def add_items(self, items: List[str], with_prefix=True) -> None:
        self.listbox.GetControl().add_items(items, with_prefix)
