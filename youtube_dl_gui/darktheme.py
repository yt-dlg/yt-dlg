# -*- coding: utf-8 -*-


from typing import List, Union

import wx


DARK_BACKGROUND_COLOUR = wx.Colour(29, 31, 33)
DARK_FOREGROUND_COLOUR = wx.Colour(197, 200, 198)


def get_widgets(parent: Union[wx.Window, wx.Panel]) -> List[wx.Window]:
    """Return a list of all the child widgets"""

    items: List[wx.Window] = [parent]

    for item in parent.GetChildren():
        items.append(item)

        if hasattr(item, "GetChildren"):
            for child in item.GetChildren():
                items.append(child)

    return items


def dark_row_formatter(listctrl: wx.ListCtrl, dark: bool = False) -> None:
    """Toggles the row in a ListCtrl"""

    items = [listctrl.GetItem(i) for i in range(listctrl.GetItemCount())]

    for index, item in enumerate(items):
        if dark:
            if index % 2:
                item.SetBackgroundColor(DARK_BACKGROUND_COLOUR)
            else:
                item.SetBackgroundColor("Light Grey")
        else:
            if index % 2:
                item.SetBackgroundColor("Light Blue")
            else:
                item.SetBackgroundColor("Yellow")

        listctrl.SetItem(item)


def dark_mode(parent: Union[wx.Window, wx.Panel], dark_mode: bool = False) -> None:
    """Toggles dark mode"""

    widgets: List[wx.Window] = get_widgets(parent)
    # panel = widgets[0]

    for widget in widgets:
        if dark_mode and not isinstance(widget, wx.TextCtrl):
            if isinstance(widget, wx.ListCtrl):
                dark_row_formatter(widget, dark=True)

            widget.SetBackgroundColour(DARK_BACKGROUND_COLOUR)
            widget.SetForegroundColour(DARK_FOREGROUND_COLOUR)
        else:
            if isinstance(widget, wx.ListCtrl):
                dark_row_formatter(widget)
                widget.SetBackgroundColour("White")
                widget.SetForegroundColour("Black")
                continue

            widget.SetBackgroundColour(wx.NullColour)
            widget.SetForegroundColour("Black")

    parent.Refresh()
