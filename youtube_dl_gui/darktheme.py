# type: ignore[misc]
# ****************************** -*-

import wx

DARK_BACKGROUND_COLOUR = wx.Colour(29, 31, 33, 255)
DARK_FOREGROUND_COLOUR = wx.Colour(197, 200, 198, 255)
DARK_BACKGROUND_COLOUR_BUTTON = wx.Colour(48, 48, 49, 255)
DARK_LIGHTGREY_COLOUR = wx.Colour(240, 240, 240, 255)


def get_widgets(parent: "wx.Window | wx.Panel") -> "list[wx.Window]":
    """Return a list of all the child widgets"""

    items: "list[wx.Window]" = [parent]

    for item in parent.GetChildren():
        items.append(item)

        if hasattr(item, "GetChildren"):
            for child in item.GetChildren():
                items.append(child)

    return items


def dark_row_formatter(listctrl: "wx.ListCtrl", dark: "bool" = False) -> "None":
    """Toggles the row in a ListCtrl"""

    items = [listctrl.GetItem(i) for i in range(listctrl.GetItemCount())]

    for index, item in enumerate(items):
        if dark:
            if index % 2:
                item.SetBackgroundColor(DARK_BACKGROUND_COLOUR)
            else:
                item.SetBackgroundColor(DARK_LIGHTGREY_COLOUR)

        listctrl.SetItem(item)


def dark_mode(parent: "wx.Window | wx.Panel", _dark_mode: "bool" = False) -> "None":
    """Toggles dark mode"""

    widgets: "list[wx.Window]" = get_widgets(parent)
    # panel = widgets[0]

    for widget in widgets:
        if _dark_mode and not isinstance(widget, (wx.TextCtrl, wx.StaticLine)):
            widget.SetBackgroundColour(DARK_BACKGROUND_COLOUR)
            widget.SetForegroundColour(DARK_FOREGROUND_COLOUR)

            if isinstance(widget, wx.ListCtrl):
                dark_row_formatter(widget, dark=True)
            elif isinstance(widget, wx.Button):
                widget.SetBackgroundColour(DARK_BACKGROUND_COLOUR_BUTTON)

    parent.Refresh()
