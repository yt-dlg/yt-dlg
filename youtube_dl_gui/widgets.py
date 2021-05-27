# -*- coding: UTF-8 -*-


from typing import Dict, List, Optional, Set, Tuple

import wx

from .darktheme import DARK_BACKGROUND_COLOUR, DARK_FOREGROUND_COLOUR


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

    def Create(self, parent: wx.ComboCtrl, **kwargs) -> bool:
        # Create components
        self.app = wx.App()
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
