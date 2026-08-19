"""Build the standalone yt-dlg executable with PyInstaller."""

import os
import subprocess
import sys


def build_executable():
    """Build the executable for the current platform."""
    data_separator = ";" if os.name == "nt" else ":"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "-w",
        "-F",
        "--icon=youtube_dl_gui/data/pixmaps/youtube-dl-gui.ico",
        "--add-data=youtube_dl_gui/data" f"{data_separator}youtube_dl_gui/data",
        "--add-data=youtube_dl_gui/locale" f"{data_separator}youtube_dl_gui/locale",
        "--exclude-module=tests",
        "--noconfirm",
        "--name=yt-dlg",
    ]
    if os.name == "nt":
        command.append("--version-file=file_version_info.txt")
    command.append("youtube_dl_gui/__main__.py")
    subprocess.run(command, check=True)


def main():
    """Run the executable build from the command line."""
    build_executable()


if __name__ == "__main__":
    main()
