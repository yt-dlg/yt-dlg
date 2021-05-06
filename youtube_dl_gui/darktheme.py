# -*- coding: utf-8 -*-


import wx


def get_widgets(parent):
    """Return a list of all the child widgets"""

    items = [parent]

    for item in parent.GetChildren():
        items.append(item)

        if hasattr(item, "GetChildren"):
            for child in item.GetChildren():
                items.append(child)

    return items


def dark_row_formatter(listctrl, dark=False):
    """Toggles the row in a ListCtrl"""

    items = [listctrl.GetItem(i) for i in range(listctrl.GetItemCount())]

    for index, item in enumerate(items):
        if dark:
            if index % 2:
                item.SetBackgroundColor("Dark Grey")
            else:
                item.SetBackgroundColor("Light Grey")
        else:
            if index % 2:
                item.SetBackgroundColor("Light Blue")
            else:
                item.SetBackgroundColor("Yellow")

        listctrl.SetItem(item)


def dark_mode(parent, dark_mode=False):
    """Toggles dark mode"""

    widgets = get_widgets(parent)
    # panel = widgets[0]

    for widget in widgets:
        if dark_mode:
            if isinstance(widget, wx.ListCtrl):
                dark_row_formatter(widget, dark=True)

            widget.SetBackgroundColour("Dark Grey")
            widget.SetForegroundColour("White")
        else:
            if isinstance(widget, wx.ListCtrl):
                dark_row_formatter(widget)
                widget.SetBackgroundColour("White")
                widget.SetForegroundColour("Black")
                continue

            widget.SetBackgroundColour(wx.NullColour)
            widget.SetForegroundColour("Black")

    parent.Refresh()

    return dark_mode
