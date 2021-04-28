# -*- coding: utf-8 -*-

"""yt-dlg module responsible for handling the log stuff. """


import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .utils import get_encoding, check_path


class LogManager(object):

    # noinspection PyUnresolvedReferences
    """Simple log manager for youtube-dl.

    This class is mainly used to log the youtube-dl STDERR.

    Attributes:
        LOG_FILENAME (string): Filename of the log file.
        TIME_TEMPLATE (string): Custom template to log the time.
        MAX_LOGSIZE (int): Maximum size(Bytes) of the log file.

    Args:
        config_path (string): Absolute path where LogManager should
            store the log file.

        add_time (boolean): If True LogManager will also log the time.

    """

    LOG_FILENAME = "log"
    MAX_LOGSIZE = 524288  # Bytes

    def __init__(self, config_path, add_time=False):
        self.config_path = config_path
        self.add_time = add_time
        self.log_file: str = str(Path(config_path).joinpath(self.LOG_FILENAME))
        self._encoding = get_encoding()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        check_path(self.config_path)

        self.handler = RotatingFileHandler(
            filename=self.log_file,
            maxBytes=LogManager.MAX_LOGSIZE,
            backupCount=5,
            encoding=self._encoding,
        )

        fmt = "%(levelname)s-%(threadName)s-%(message)s"

        if self.add_time:
            fmt = "%(asctime)s-" + fmt

        self.handler.setFormatter(logging.Formatter(fmt=fmt))
        self.logger.addHandler(self.handler)

    def log_size(self) -> int:
        """Return log file size in Bytes. """
        path = Path(self.log_file)

        if not path.exists():
            return 0

        return path.stat().st_size

    def clear(self):
        """Clear log file. """
        with open(self.log_file, "w") as log:
            log.write("")

    def log(self, data):
        """Log data to the log file.

        Args:
            data (string): String to write to the log file.

        """
        self.logger.debug(str(data))
