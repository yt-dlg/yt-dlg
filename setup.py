"""yt-dlg setup file.

Examples:
    Windows/Linux::

        python setup.py pyinstaller

    Linux::

        python setup.py install

    Build source distribution::

        python setup.py sdist

    Build platform distribution::

        python setup.py bdist

    Build the translations::

        python setup.py build_trans

    Build with updates disabled::

        python setup.py no_updates


    Basic steps of the setup::

        * Run pre-build tasks
        * Call setup handler based on OS & options
            * Set up hicolor icons (if supported by platform)
            * Set up fallback pixmaps icon (if supported by platform)
            * Set up package level pixmaps icons (*.png)
            * Set up package level i18n files (*.mo)
            * Set up scripts (executables) (if supported by platform)
        * Run setup

"""


import glob
import importlib
import logging
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from setuptools import Command, setup

try:
    import youtube_dl_gui
except ModuleNotFoundError:
    # For editable mode
    HERE = Path(__file__).resolve().parent
    sys.path.insert(0, str(HERE))
    import youtube_dl_gui

PYINSTALLER = len(sys.argv) >= 2 and sys.argv[1] == "pyinstaller"

try:
    from PyInstaller import compat as pyi_compat

    if pyi_compat.is_win:
        # noinspection PyUnresolvedReferences
        from PyInstaller.utils.win32.versioninfo import (
            FixedFileInfo,
            SetVersion,
            StringFileInfo,
            StringStruct,
            StringTable,
            VarFileInfo,
            VarStruct,
            VSVersionInfo,
        )
except ImportError:
    pyi_compat = None
    if PYINSTALLER:
        print("Cannot import pyinstaller", file=sys.stderr)
        exit(1)


IS_WINDOWS = os.name == "nt"
DESCRIPTION = youtube_dl_gui.__description__


def version2tuple(commit=0):
    version_list = str(youtube_dl_gui.__version__).split(".")

    if len(version_list) > 3:
        del version_list[3]

    _release = commit

    _year, _month, _day = tuple(map(int, version_list))
    return _year, _month, _day, _release


def version2str(commit=0):
    version_tuple = version2tuple(commit)
    return "%s.%s.%s.%s" % version_tuple


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# noinspection PyAttributeOutsideInit,PyArgumentList
class BuildTranslations(Command):
    description = "Build the translation files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from devscripts.build_translations import build_translations

        try:
            build_translations()
        except OSError as error:
            logger.error(f"{error}, exiting...")
            sys.exit(1)


# noinspection PyAttributeOutsideInit,PyArgumentList
class BuildNoUpdate(Command):
    description = "Build with updates disabled"
    user_options = []

    def initialize_options(self):
        self.build_lib = os.path.dirname(os.path.abspath(__file__))

    def finalize_options(self):
        pass

    def run(self):
        self.__disable_updates()

    def __disable_updates(self):
        lib_dir = os.path.join(self.build_lib, youtube_dl_gui.__packagename__)
        target_file = "optionsmanager.py"
        # Options file should be available from previous build commands
        optionsfile = os.path.join(lib_dir, target_file)

        with open(optionsfile) as input_file:
            data = input_file.readlines()

        if data is None:
            logger.error("Building with updates disabled failed!")
            sys.exit(1)

        for index, line in enumerate(data):
            if '"disable_update": False' in line:
                logger.info("Disabling updates...")
                data[index] = line.replace("False", "True")
                break

        with open(optionsfile, "w") as output_file:
            output_file.writelines(data)


class BuildPyinstallerBin(Command):
    description = "Build the executable"
    user_options = []
    version_file = None
    if pyi_compat and pyi_compat.is_win:
        version_file = VSVersionInfo(
            ffi=FixedFileInfo(
                filevers=version2tuple(),
                prodvers=version2tuple(),
                mask=0x3F,
                flags=0x0,
                OS=0x4,
                fileType=0x1,
                subtype=0x0,
                date=(0, 0),
            ),
            kids=[
                VarFileInfo([VarStruct("Translation", [0, 1200])]),
                StringFileInfo(
                    [
                        StringTable(
                            "000004b0",
                            [
                                StringStruct(
                                    "CompanyName", youtube_dl_gui.__mcontact__
                                ),
                                StringStruct("FileDescription", DESCRIPTION),
                                StringStruct("FileVersion", version2str()),
                                StringStruct("InternalName", "yt-dlg.exe"),
                                StringStruct(
                                    "LegalCopyright",
                                    f"{youtube_dl_gui.__projecturl__}LICENSE",
                                ),
                                StringStruct("OriginalFilename", "yt-dlg.exe"),
                                StringStruct("ProductName", youtube_dl_gui.__appname__),
                                StringStruct("ProductVersion", version2str()),
                            ],
                        )
                    ]
                ),
            ],
        )

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self, version=version_file):
        """Run pyinstaller"""
        path_sep = ";" if IS_WINDOWS else ":"
        subprocess.run(
            [
                "pyinstaller",
                "-w",
                "-F",
                f"--icon={youtube_dl_gui.__packagename__}/data/pixmaps/youtube-dl-gui.ico",
                "--add-data="
                + youtube_dl_gui.__packagename__
                + "/data"
                + path_sep
                + youtube_dl_gui.__packagename__
                + "/data",
                "--add-data="
                + youtube_dl_gui.__packagename__
                + "/locale"
                + path_sep
                + youtube_dl_gui.__packagename__
                + "/locale",
                "--exclude-module=tests",
                "--name=yt-dlg",
                f"{youtube_dl_gui.__packagename__}/__main__.py",
            ]
        )

        if version:
            SetVersion("./dist/yt-dlg.exe", version)


cmdclass = {
    "build_trans": BuildTranslations,
    "no_updates": BuildNoUpdate,
}

def setup_linux():
    """Setup params for Linux"""
    data_files_linux = []
    # Add hicolor icons
    for path in glob.glob("youtube_dl_gui/data/icons/hicolor/*x*"):
        size = os.path.basename(path)

        dst = f"share/icons/hicolor/{size}/apps"
        src = f"{path}/apps/youtube-dl-gui.png"

        data_files_linux.append((dst, [src]))
    data_files_linux.extend(
        (
            (
                "share/pixmaps",
                ["youtube_dl_gui/data/pixmaps/youtube-dl-gui.png"],
            ),
            ("share/man/man1", ["youtube-dl-gui.1"]),
        )
    )

    return {
        "data_files": data_files_linux,
    }


def setup_windows():
    """Setup params for Windows"""
    return {}


params = {}

if PYINSTALLER:
    cmdclass.update({"pyinstaller": BuildPyinstallerBin})
else:
    params = setup_windows() if IS_WINDOWS else setup_linux()


if __name__ == "__main__":
    setup(license=youtube_dl_gui.__license__, cmdclass=cmdclass, **params)
