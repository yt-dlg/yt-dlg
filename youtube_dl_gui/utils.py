# -*- coding: utf-8 -*-

"""yt-dlg module that contains util functions.

Attributes:
    _RANDOM_OBJECT (object): Object that it's used as a default parameter.

    YOUTUBEDL_BIN (string): Youtube-dl binary filename.

"""

import os
import sys
import math
import locale
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from .info import __appname__


_RANDOM_OBJECT: object = object()

YOUTUBEDL_BIN: str = "youtube-dl"
if os.name == "nt":
    YOUTUBEDL_BIN += ".exe"

FILESIZE_METRICS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]

KILO_SIZE = 1024.0


def get_encoding() -> str:
    """Return system encoding. """
    try:
        encoding = locale.getpreferredencoding()
        "TEST".encode(encoding)
    except locale.Error:
        encoding = "UTF-8"

    return encoding


def convert_item(item, to_unicode=False):
    """Convert item between 'unicode' and 'str'.

    Args:
        item (-): Can be any python item.

        to_unicode (boolean): When True it will convert all the 'str' types
            to 'unicode'. When False it will convert all the 'unicode'
            types back to 'str'.

    """
    if to_unicode and isinstance(item, str):
        # Convert str to unicode
        return str(item)

    if not to_unicode and isinstance(item, bytes):
        # Convert bytes to str
        return bytes(item).decode(encoding=get_encoding(), errors="ignore")

    if isinstance(item, (dict, list, tuple)):
        # Handle iterables
        temp_list = []

        for sub_item in item:
            if isinstance(item, dict):
                temp_list.append(
                    (
                        convert_item(sub_item, to_unicode),
                        convert_item(item[sub_item], to_unicode),
                    )
                )
            elif isinstance(item, (list, tuple)):
                temp_list.append(convert_item(sub_item, to_unicode))

        return type(item)(temp_list)

    return item


def convert_on_bounds(func):
    """Decorator to convert string inputs & outputs.

    Covert string inputs & outputs between 'str' and 'unicode' at the
    application bounds using the preferred system encoding. It will convert
    all the string params (args, kwargs) to 'str' type and all the
    returned strings values back to 'unicode'.

    """

    def wrapper(*args, **kwargs):
        returned_value = func(*convert_item(args), **convert_item(kwargs))

        return convert_item(returned_value, True)

    return wrapper


locale_getdefaultlocale = locale.getdefaultlocale


def startfile(file_path: str) -> None:
    if os.name == "nt":
        os.startfile(file_path)
    else:
        subprocess.call(("xdg-open", file_path))


os_startfile = startfile


def remove_file(filename: str) -> bool:
    file_path = Path(filename)
    if file_path.exists():
        file_path.unlink()
        return True

    return False


def remove_shortcuts(path: str) -> str:
    """Return given path after removing the shortcuts. """
    return path.replace("~", str(Path().home()))


def absolute_path(filename: str) -> str:
    """Return absolute path to the given file. """
    return str(Path(filename).resolve())


def open_file(file_path: str) -> bool:
    """Open file in file_path using the default OS application.

    Returns:
        True on success else False.

    """

    if not Path(file_path).exists():
        return False

    os_startfile(file_path)

    return True


def encode_tuple(tuple_to_encode: Tuple[str, str]) -> str:
    """Turn size tuple into string. """
    return "%s/%s" % (tuple_to_encode[0], tuple_to_encode[1])


def decode_tuple(encoded_tuple: str) -> Tuple[int, int]:
    """Turn tuple string back to tuple. """
    s = encoded_tuple.split("/")
    return int(s[0]), int(s[1])


def check_path(path: str) -> None:
    """Create path if not exist. """
    if not Path(path).exists():
        os.makedirs(path)


def get_config_path() -> str:
    """Return user config path.

    Note:
        Windows = %AppData% + app_name
        Linux   = ~/.config + app_name

    """
    path: str = ""

    if os.name == "nt":
        path = os.getenv("APPDATA", "")
    else:
        path = str(Path().home().joinpath(".config"))

    return str(Path(path).joinpath(__appname__.lower()))


def shutdown_sys(password=None) -> bool:
    """Shuts down the system.
    Returns True if no errors occur else False.

    Args:
        password (string): SUDO password for linux.

    Note:
        On Linux you need to provide sudo password if you don't
        have elevated privileges.

    """
    info = None
    cmd = []
    encoding: str = get_encoding()

    kwargs = dict(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        encoding=encoding,
        creationflags=0,
    )

    if os.name == "nt":
        cmd = ["shutdown", "/s", "/t", "1"]

        # Hide subprocess window
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE

        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True

        if password:
            password = "%s\n" % password
            cmd = ["sudo", "-S", "/sbin/shutdown", "-h", "now"]
        else:
            cmd = ["/sbin/shutdown", "-h", "now"]

    shutdown_proc = subprocess.Popen(
        cmd, startupinfo=info, **kwargs
    )  # type: ignore[call-overload]

    output = shutdown_proc.communicate(password)[1]

    return not output or output == "Password:"


def to_string(data) -> str:
    """Convert data to string.
    Works for both Python2 & Python3."""
    return "%s" % data


def get_time(seconds: float) -> Dict[str, int]:
    """Convert given seconds to days, hours, minutes and seconds.

    Args:
        seconds (float): Time in seconds.

    Returns:
        Dictionary that contains the corresponding days, hours, minutes
        and seconds of the given seconds.

    """
    dtime = dict(seconds=0, minutes=0, hours=0, days=0)

    dtime["days"] = int(seconds / 86400)
    dtime["hours"] = int(seconds % 86400 / 3600)
    dtime["minutes"] = int(seconds % 86400 % 3600 / 60)
    dtime["seconds"] = int(seconds % 86400 % 3600 % 60)

    return dtime


def get_search_dirs(dir_name: str) -> List[Path]:
    return [
        Path(sys.argv[0]).joinpath(dir_name),
        Path(__file__).parent.joinpath(dir_name),
    ]


def get_locale_file() -> Optional[str]:
    """Search for yt_dlg locale file.

    Returns:
        The path to yt_dlg locale file if exists else None.

    Note:
        Paths that get_locale_file() func searches.

        __main__ dir, library dir

    """
    SEARCH_DIRS = get_search_dirs("locale")

    for directory in SEARCH_DIRS:
        if directory.is_dir():
            return str(directory)

    return None


def get_icon_file() -> Optional[str]:
    """Search for yt_dlg app icon.

    Returns:
        The path to yt_dlg icon file if exists, else returns None.

    """
    pixmaps_dir = get_pixmaps_dir()

    if pixmaps_dir:
        ICON_NAME = "youtube-dl-gui.png"

        icon_file = Path(pixmaps_dir).joinpath(ICON_NAME)

        if icon_file.exists():
            return str(icon_file)

    return None


def get_pixmaps_dir() -> Optional[str]:
    """Return absolute path to the pixmaps icons folder.

    Note:
        Paths we search: __main__ dir, library dir

    """
    SEARCH_DIRS = get_search_dirs("data")

    for directory in SEARCH_DIRS:
        pixmaps_dir = directory.joinpath("pixmaps")

        if pixmaps_dir.is_dir():
            return str(pixmaps_dir)

    return None


def to_bytes(string: str):
    """Convert given youtube-dl size string to bytes."""
    value = 0.0
    index = 0

    for index, metric in enumerate(reversed(FILESIZE_METRICS)):
        if metric in string:
            value = float(string.split(metric)[0])
            break

    exponent = index * (-1) + (len(FILESIZE_METRICS) - 1)

    return round(value * (KILO_SIZE ** exponent), 2)


def format_bytes(bytes_) -> str:
    """Format bytes to youtube-dl size output strings."""
    exponent = 0 if bytes == 0.0 else int(math.log(bytes_, KILO_SIZE))
    suffix = FILESIZE_METRICS[exponent]
    output_value = bytes_ / (KILO_SIZE ** exponent)

    return "%.2f%s" % (output_value, suffix)


def build_command(options_list: List[str], url: str) -> str:
    """Build the youtube-dl command line string."""

    def escape(option):
        """Wrap option with double quotes if it contains special symbols."""
        special_symbols = [" ", "(", ")"]

        for symbol in special_symbols:
            if symbol in option:
                return '"{}"'.format(option)

        return option

    # If option has special symbols wrap it with double quotes
    # Probably not the best solution since if the option already contains
    # double quotes it will be a mess, see issue #173
    options = [escape(option) for option in options_list]

    # Always wrap the url with double quotes
    url = '"{}"'.format(url)

    return " ".join([YOUTUBEDL_BIN] + options + [url])


def get_default_lang() -> str:
    """Get default language using the 'locale' module."""
    default_lang, _ = locale_getdefaultlocale()

    return default_lang or "en_US"


def get_key(string: str, dictionary: Dict[str, str], default: str = "") -> str:
    """Get key from a value in Dictionary. Return default if key doesn't exist"""
    for key, value in dictionary.items():
        if value == string:
            default = key
            return default
    return default
