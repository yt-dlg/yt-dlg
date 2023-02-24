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
import logging
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from setuptools import Command, setup


def load_vars(file=Path("youtube_dl_gui/info.py")):
    source = file.read_text(encoding="utf-8")
    _vars = defaultdict(lambda: "")

    # Docs file
    match = re.search(r'["]{3}(.*)["]{3}', source)
    if match:
        _vars["__doc__"] = f"{match.groups(0)[0]}"

    match = re.findall(r'([_]{2}[a-z]+[_]{2})\s+=\s+["\']{1}(.+)["\']{1}', source)
    if match:
        _vars.update(dict(match))
    return _vars


PYINSTALLER = len(sys.argv) >= 2 and sys.argv[1] == "pyinstaller"

vars_file = load_vars()
vars_file.update(load_vars(Path("youtube_dl_gui/version.py")))

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


DESCRIPTION = vars_file["__description__"]
LONG_DESCRIPTION = open("README.md", encoding="utf-8").read()


def on_windows():
    """Returns True if OS is Windows."""
    return os.name == "nt"


def version2tuple(commit=0):
    version_list = str(vars_file["__version__"]).split(".")

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
        self.search_pattern = None

    def finalize_options(self):
        self.search_pattern = os.path.join(
            vars_file["__packagename__"],
            "locale",
            "*",
            "LC_MESSAGES",
            "youtube_dl_gui.po",
        )

    def run(self):
        import polib

        po_file = ""

        try:
            for po_file in glob.glob(self.search_pattern):
                mo_file = po_file.replace(".po", ".mo")
                po = polib.pofile(po_file)

                logger.info(f"Building MO file for '{po_file}'")
                po.save_as_mofile(mo_file)
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
        lib_dir = os.path.join(self.build_lib, vars_file["__packagename__"])
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
                                StringStruct("CompanyName", vars_file["__mcontact__"]),
                                StringStruct("FileDescription", DESCRIPTION),
                                StringStruct("FileVersion", version2str()),
                                StringStruct("InternalName", "yt-dlg.exe"),
                                StringStruct(
                                    "LegalCopyright",
                                    f"{vars_file['__projecturl__']}LICENSE",
                                ),
                                StringStruct("OriginalFilename", "yt-dlg.exe"),
                                StringStruct("ProductName", vars_file["__appname__"]),
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
        path_sep = ";" if on_windows() else ":"
        subprocess.run(
            [
                "pyinstaller",
                "-w",
                "-F",
                f"--icon={vars_file['__packagename__']}/data/pixmaps/youtube-dl-gui.ico",
                "--add-data="
                + vars_file["__packagename__"]
                + "/data"
                + path_sep
                + vars_file["__packagename__"]
                + "/data",
                "--add-data="
                + vars_file["__packagename__"]
                + "/locale"
                + path_sep
                + vars_file["__packagename__"]
                + "/locale",
                "--exclude-module=tests",
                "--name=yt-dlg",
                f"{vars_file['__packagename__']}/__main__.py",
            ]
        )

        if version:
            SetVersion("./dist/yt-dlg.exe", version)


cmdclass = {
    "build_trans": BuildTranslations,
    "no_updates": BuildNoUpdate,
}

# Add pixmaps icons (*.png) & i18n files
package_data = {
    vars_file["__packagename__"]: ["data/pixmaps/*.png", "locale/*/LC_MESSAGES/*.mo"]
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
        "package_data": package_data,
    }


def setup_windows():
    """Setup params for Windows"""
    return {
        "package_data": package_data,
    }


params = {}

if PYINSTALLER:
    cmdclass.update({"pyinstaller": BuildPyinstallerBin})
else:
    params = setup_windows() if on_windows() else setup_linux()
    params["entry_points"] = {
        "console_scripts": [
            f"{vars_file['__appname__']} = {vars_file['__packagename__']}.app:main"
        ]
    }


if __name__ == "__main__":
    setup(
        name=f"{vars_file['__appname__']}".replace("-", "_"),
        version=vars_file["__version__"],
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        url=vars_file["__projecturl__"],
        download_url=f"{vars_file['__githuburl__']}releases/latest",
        project_urls={
            "Source": vars_file["__githuburl__"],
            "Tracker": f"{vars_file['__githuburl__']}issues",
            "Funding": f"{vars_file['__projecturl__']}donate.html",
        },
        author=vars_file["__author__"],
        author_email=vars_file["__contact__"],
        maintainer=vars_file["__maintainer__"],
        maintainer_email=vars_file["__mcontact__"],
        license=vars_file["__license__"],
        packages=[vars_file["__packagename__"]],
        install_requires=[
            "pypubsub>=4.0.3",
            "wxPython<=4.2.1a1,>=4.0.7.post2",
        ],
        extras_require={
            "binaries": ["polib>=1.1.0", "pyinstaller<=5.8.0,>=3.6"],
        },
        python_requires=">=3.7",
        classifiers=[
            "Topic :: Multimedia :: Video",
            "Development Status :: 5 - Production/Stable",
            "Environment :: MacOS X :: Cocoa",
            "Environment :: Win32 (MS Windows)",
            "Environment :: X11 Applications :: GTK",
            "License :: Public Domain",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
        cmdclass=cmdclass,
        **params,
    )
