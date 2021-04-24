# -*- coding: utf-8 -*-

"""Youtubedlg __main__ file.

__main__ file is a python 'executable' file which calls the youtubedlg
main() function in order to start the app. It can be used to start
the app from the package directory OR it can be used to start the app
from a different directory after you have installed the youtube_dl_gui
package.

Example:
    In order to run the app from the package directory.

        $ cd <package director>
        $ python __main__.py

    In order to run the app from /usr/local/bin etc.. AFTER
    you have installed the package using setup.py.

        $ youtube-dl-gui

"""


from pathlib import Path
import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    PATH = Path(__file__).parent
    sys.path.insert(0, str(PATH))

import youtube_dl_gui


if __name__ == "__main__":
    youtube_dl_gui.main()
