"""yt-dlg __main__ file.

__main__ file is a python 'executable' file which calls the youtube_dl_gui.app
main() function in order to start the app. It can be used to start
the app from the package directory OR it can be used to start the app
from a different directory after you have installed the youtube_dl_gui
package.

Example:
    In order to run the app from the package directory.

        $ cd <package directory>
        $ python __main__.py

    In order to run the app AFTER you have installed the package using
    setup.py.

        $ yt-dlg

"""


import sys
from pathlib import Path

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    PATH = Path(__file__).resolve().parent
    sys.path.insert(0, str(PATH))

from youtube_dl_gui.app import main  # type: ignore[attr-defined]

sys.exit(main())
