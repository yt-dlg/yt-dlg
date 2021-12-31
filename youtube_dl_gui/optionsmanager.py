# type: ignore[misc]
"""yt-dlg module to handle settings. """
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .formats import FORMATS, OUTPUT_FORMATS
from .utils import (
    YOUTUBEDL_BIN,
    check_path,
    decode_tuple,
    encode_tuple,
    get_default_lang,
)


class OptionsManager:
    # noinspection PyUnresolvedReferences
    """Handles yt-dlg options.

    This class is responsible for storing and retrieving the options.

    Attributes:
        SETTINGS_FILENAME (str): Filename of the settings file.
        SENSITIVE_KEYS (tuple): Contains the keys that we don't want
            to store on the settings file. (SECURITY ISSUES).

    Args:
        config_path (str): Absolute path where OptionsManager
            should store the settings file.

    Note:
        See load_default() method for available options.

    Example:
        Access the options using the 'options' variable.

        opt_manager = OptionsManager('.')
        opt_manager.options['save_path'] = '~/Downloads'

    """

    SETTINGS_FILENAME = "settings.json"
    SENSITIVE_KEYS = ("sudo_password", "password", "video_password")
    MAIN_WIN_SIZE = (740, 490)
    OPTS_WIN_SIZE = (640, 490)

    def __init__(self, config_path: str):
        self.config_path: str = config_path
        self.settings_file: str = str(Path(config_path) / Path(self.SETTINGS_FILENAME))
        self.options: dict[str, Any] = {}
        self.load_default()
        self.load_from_file()

    def load_default(self) -> None:
        """Load the default options.

        Note:
            This method is automatically called by the constructor.

        Options Description:

            save_path (str): Path where youtube-dl should store the
                downloaded file. Default is $HOME.

            video_format (str): Video format to download.
                When this options is set to '0' youtube-dl will choose
                the best video format available for the given URL.

            second_video_format (str): Video format to mix with the first
                one (-f 18+17).

            to_audio (bool): If True youtube-dl will post process the
                video file.

            keep_video (bool): If True youtube-dl will keep the video file
                after post processing it.

            audio_format (str): Audio format of the post processed file.
                Available values are "mp3", "wav", "aac", "m4a", "vorbis",
                "opus" & "flac".

            audio_quality (str): Audio quality of the post processed file.
                Available values are "9", "5", "0". The lowest the value the
                better the quality.

            restrict_filenames (bool): If True youtube-dl will restrict
                the downloaded file filename to ASCII characters only.

            output_format (str): This option sets the downloaded file
                output template. See formats.OUTPUT_FORMATS for more info.

            output_template (str): Can be any output template supported
                by youtube-dl.

            playlist_start (int): Playlist index to start downloading.

            playlist_end (int): Playlist index to stop downloading.

            max_downloads (int): Maximum number of video files to download
                from the given playlist.

            min_filesize (float): Minimum file size of the video file.
                If the video file is smaller than the given size then
                youtube-dl will abort the download process.

            max_filesize (float): Maximum file size of the video file.
                If the video file is larger than the given size then
                youtube-dl will abort the download process.

            min_filesize_unit (str): Minimum file size unit.
                Available values: '', 'k', 'm', 'g', 'y', 'p', 'e', 'z', 'y'.

            max_filesize_unit (str): Maximum file size unit.
                See 'min_filesize_unit' option for available values.

            write_subs (bool): If True youtube-dl will try to download
                the subtitles file for the given URL.

            write_all_subs (bool): If True youtube-dl will try to download
                all the available subtitles files for the given URL.

            write_auto_subs (bool): If True youtube-dl will try to download
                the automatic subtitles file for the given URL.

            embed_subs (bool): If True youtube-dl will merge the subtitles
                file with the video. (ONLY mp4 files).

            subs_lang (str): Language of the subtitles file to download.
                Needs 'write_subs' option.

            ignore_errors (bool): If True youtube-dl will ignore the errors
                and continue the download process.

            open_dl_dir (bool): If True yt-dlg will open the
                destination folder after download process has been completed.

            write_description (bool): If True youtube-dl will write video
                description to a .description file.

            write_info (bool): If True youtube-dl will write video
                metadata to a .info.json file.

            write_thumbnail (bool): If True youtube-dl will write
                thumbnail image to disk.

            retries (int): Number of youtube-dl retries.

            user_agent (str): Specify a custom user agent for youtube-dl.

            referer (str): Specify a custom referer to use if the video
                access is restricted to one domain.

            proxy (str): Use the specified HTTP/HTTPS proxy.

            shutdown (bool): If True yt-dlg will turn the computer
                off after the download process has been completed.

            sudo_password (str): SUDO password for the shutdown process if
                the user does not have elevated privileges.

            username (str): Username to login with.

            password (str): Password to login with.

            video_password (str): Video password for the given URL.

            cli_backend (str): CLI backen used to download.
                Currently youtube-dl, yt-dlp
                Default youtube-dl

            youtubedl_path (str): Absolute path to the youtube-dl binary.
                Default is the self.config_path. You can change this option
                to point on /usr/local/bin etc.. if you want to use the
                youtube-dl binary on your system. This is also the directory
                where yt-dlg will auto download the youtube-dl if not
                exists so you should make sure you have write access if you
                want to update the youtube-dl binary from within yt-dlg.

            cmd_args (str): String that contains extra youtube-dl options
                seperated by spaces.

            enable_log (bool): If True yt-dlg will enable
                the LogManager. See app module.

            log_time (bool): See logmanager.LogManager add_time attribute.

            workers_number (int): Number of download workers that download manager
                will spawn. Must be greater than zero.

            locale_name (str): Locale name (e.g. ru_RU).

            main_win_size (tuple): Main window size (width, height).
                If window becomes to small the program will reset its size.
                See _settings_are_valid method MIN_FRAME_SIZE.

            opts_win_size (tuple): Options window size (width, height).
                If window becomes to small the program will reset its size.
                See _settings_are_valid method MIN_FRAME_SIZE.

            save_path_dirs (list): List that contains temporary save paths.

            selected_video_formats (list): List that contains the selected
                video formats to display on the main window.

            selected_audio_formats (list): List that contains the selected
                audio formats to display on the main window.

            selected_format (str): Current format selected on the main window.

            youtube_dl_debug (bool): When True will pass '-v' flag to youtube-dl.

            ignore_config (bool): When True will ignore youtube-dl config file options.

            confirm_exit (bool): When True create popup to confirm exiting youtube-dl-gui.

            native_hls (bool): When True youtube-dl will use the native HLS implementation.

            # TODO:
            ffmpeg_hls (bool): (--hls-prefer-ffmpeg) Use ffmpeg insted of the native HLS
                downloader. (IMPLEMENT with radio buttons)
                EX: --hls-prefer-ffmpeg \
                    --external-downloader ffmpeg --external-downloader-args "-ss 234 -to 621"
            # TODO:
            external_downloader (str): Use the specified external downloader.
                Currently supports aria2c, avconv, axel, curl, ffmpeg, httpie, wget
                Default ffmpeg
            # TODO:
            external_downloader_args (list): List of string give to arguments
                to the external downloader.

            show_completion_popup (bool): When True youtube-dl-gui will create a popup
                to inform the user for the download completion.

            confirm_deletion (bool): When True ask user before item removal.

            nomtime (bool): When True will not use the Last-modified header to
                set the file modification time.

            embed_thumbnail (bool): When True will embed the thumbnail in
                the audio file as cover art.

            add_metadata (bool): When True will write metadata to file.

            disable_update (bool): When True the update process will be disabled.

        """
        # REFACTOR Remove old options & check options validation
        self.options = {
            "save_path": str(Path().home()),
            "save_path_dirs": [
                str(Path().home()),
                str(Path().home() / Path("Downloads")),
                str(Path().home() / Path("Desktop")),
                str(Path().home() / Path("Videos")),
                str(Path().home() / Path("Music")),
            ],
            "video_format": "0",
            "second_video_format": "0",
            "to_audio": False,
            "keep_video": False,
            "audio_format": "",
            "audio_quality": "5",
            "restrict_filenames": False,
            "dark_mode": False,
            "output_format": "1",
            "output_template": str(Path("%(uploader)s") / Path("%(title)s.%(ext)s")),
            "playlist_start": 1,
            "playlist_end": 0,
            "max_downloads": 0,
            "min_filesize": 0,
            "max_filesize": 0,
            "min_filesize_unit": "",
            "max_filesize_unit": "",
            "write_subs": False,
            "write_all_subs": False,
            "write_auto_subs": False,
            "embed_subs": False,
            "subs_lang": "en",
            "ignore_errors": True,
            "open_dl_dir": False,
            "write_description": False,
            "write_info": False,
            "write_thumbnail": False,
            "retries": 10,
            "user_agent": "",
            "referer": "",
            "proxy": "",
            "shutdown": False,
            "sudo_password": "",
            "username": "",
            "password": "",
            "video_password": "",
            "cli_backend": YOUTUBEDL_BIN,
            "youtubedl_path": self.config_path,
            "cmd_args": "",
            "enable_log": True,
            "log_time": True,
            "workers_number": 3,
            "locale_name": get_default_lang(),
            "main_win_size": self.MAIN_WIN_SIZE,
            "opts_win_size": self.OPTS_WIN_SIZE,
            "selected_video_formats": ["webm", "mp4"],
            "selected_audio_formats": ["mp3", "m4a", "vorbis"],
            "selected_format": "0",
            "youtube_dl_debug": False,
            "ignore_config": True,
            "confirm_exit": True,
            "native_hls": True,
            "show_completion_popup": True,
            "confirm_deletion": True,
            "nomtime": False,
            "embed_thumbnail": False,
            "add_metadata": False,
            "disable_update": False,
        }

        # Set the youtubedl_path again if the disable_update option is set
        new_path: str = "/usr/bin"

        if (
            self.options["disable_update"]
            and os.name != "nt"
            and Path(new_path).exists()
        ):
            self.options["youtubedl_path"] = new_path

    def load_from_file(self) -> None:
        """Load options from settings file."""
        settings_path: Path = Path(self.settings_file)

        if not settings_path.exists():
            return

        with open(settings_path) as settings_file:
            try:
                options: dict[str, Any] = json.load(settings_file)

                if self._settings_are_valid(options):
                    self.options = options
            except json.JSONDecodeError:
                self.load_default()

    def save_to_file(self) -> None:
        """Save options to settings file."""
        check_path(self.config_path)

        with open(self.settings_file, "w") as settings_file:
            options = self._get_options()
            json.dump(options, settings_file, indent=4, separators=(",", ": "))

    # noinspection PyPep8Naming
    def _settings_are_valid(self, settings_dictionary: dict[str, Any]) -> bool:
        """Check settings.json dictionary.

        Args:
            settings_dictionary (dict): Options dictionary loaded
                from the settings file. See load_from_file() method.

        Returns:
            True if settings.json dictionary is valid, else False.

        """
        VALID_VIDEO_FORMAT = (
            "0",
            "17",
            "36",
            "5",
            "34",
            "35",
            "43",
            "44",
            "45",
            "46",
            "18",
            "22",
            "37",
            "38",
            "160",
            "133",
            "134",
            "135",
            "136",
            "137",
            "264",
            "138",
            "242",
            "243",
            "244",
            "247",
            "248",
            "271",
            "272",
            "82",
            "83",
            "84",
            "85",
            "100",
            "101",
            "102",
            "139",
            "140",
            "141",
            "171",
            "172",
        )

        VALID_AUDIO_FORMAT = ("mp3", "wav", "aac", "m4a", "vorbis", "opus", "flac", "")

        VALID_AUDIO_QUALITY = ("0", "5", "9")

        VALID_FILESIZE_UNIT = ("", "k", "m", "g", "t", "p", "e", "z", "y")

        VALID_SUB_LANGUAGE = (
            "en",
            "el",
            "pt",
            "fr",
            "it",
            "ru",
            "es",
            "de",
            "he",
            "sv",
            "tr",
        )

        MIN_FRAME_SIZE = 100

        # Decode string formatted tuples back to normal tuples
        settings_dictionary["main_win_size"] = decode_tuple(
            settings_dictionary["main_win_size"]
        )
        settings_dictionary["opts_win_size"] = decode_tuple(
            settings_dictionary["opts_win_size"]
        )

        for key in self.options:
            if key not in settings_dictionary:
                return False

            if not isinstance(self.options[key], type(settings_dictionary[key])):
                return False

        # Check if each key has a valid value
        rules_dict = {
            "video_format": FORMATS.keys(),
            "second_video_format": VALID_VIDEO_FORMAT,
            "audio_format": VALID_AUDIO_FORMAT,
            "audio_quality": VALID_AUDIO_QUALITY,
            "output_format": OUTPUT_FORMATS.keys(),
            "min_filesize_unit": VALID_FILESIZE_UNIT,
            "max_filesize_unit": VALID_FILESIZE_UNIT,
            "subs_lang": VALID_SUB_LANGUAGE,
        }

        for key, valid_list in rules_dict.items():
            if settings_dictionary[key] not in valid_list:
                return False

        # Check workers number value
        if settings_dictionary["workers_number"] < 1:
            return False

        # Check main-options frame size
        for size in settings_dictionary["main_win_size"]:
            if size < MIN_FRAME_SIZE:
                return False

        return all(
            size >= MIN_FRAME_SIZE for size in settings_dictionary["opts_win_size"]
        )

    def _get_options(self) -> dict[str, Any]:
        """Return options dictionary without SENSITIVE_KEYS."""
        temp_options = self.options.copy()

        for key in self.SENSITIVE_KEYS:
            temp_options[key] = ""

        # Encode normal tuples to string formatted tuples
        temp_options["main_win_size"] = encode_tuple(temp_options["main_win_size"])
        temp_options["opts_win_size"] = encode_tuple(temp_options["opts_win_size"])

        return temp_options
