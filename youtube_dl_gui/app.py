# -*- coding: utf-8 -*-

"""yt-dlg wx Application

Example:
    In order to load the GUI from a python script.

        from youtube_dl_gui import app

        app.main()

"""

import sys
from pathlib import Path

import wx

from .info import __appname__, __packagename__
from .logmanager import LogManager
from .mainframe import MainFrame
from .optionsmanager import OptionsManager
from .utils import get_config_path, get_locale_file, YOUTUBEDL_BIN


_ = wx.GetTranslation

# Set config path and create options and log managers
config_path = get_config_path()

opt_manager = OptionsManager(config_path)
log_manager = None

if opt_manager.options.get("enable_log", True):
    log_manager = LogManager(config_path, opt_manager.options.get("log_time", True))

# Set gettext before MainFrame import
# because the GUI strings are class level attributes
locale_dir = get_locale_file()

# Install a custom displayhook to keep Python from setting the global
# _ (underscore) to the value of the last evaluated expression.  If
# we don't do this, our mapping of _ to gettext can get overwritten.
# This is useful/needed in interactive debugging with PyShell.


def _displayHook(obj):
    if obj is not None:
        print(repr(obj))


class BaseApp(wx.App):
    def OnInit(self):
        super().OnInit()
        sys.displayhook = _displayHook

        self.appName = __appname__
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(locale_dir)
        self.updateLanguage(opt_manager.options.get("locale_name", "en_US"))

        return True

    def updateLanguage(self, lang: str):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param str `lang`: one of the supported language codes

        """

        # Supported Languages
        # Lang code = <ISO 639-1>_<ISO 3166-1 alpha-2>
        supLang = {
            "ar_SA": wx.LANGUAGE_ARABIC,
            "cs_CZ": wx.LANGUAGE_CZECH,
            "en_US": wx.LANGUAGE_ENGLISH_US,
            "fr_FR": wx.LANGUAGE_FRENCH,
            "es_CU": wx.LANGUAGE_SPANISH,
            "it_IT": wx.LANGUAGE_ITALIAN,
            "ja_JP": wx.LANGUAGE_JAPANESE,
            "ko_KR": wx.LANGUAGE_KOREAN,
            "pt_BR": wx.LANGUAGE_PORTUGUESE_BRAZILIAN,
            "ru_RU": wx.LANGUAGE_RUSSIAN,
            "es_ES": wx.LANGUAGE_SPANISH,
            "sq_AL": wx.LANGUAGE_ALBANIAN,
        }

        selLang = supLang.get(lang, wx.LANGUAGE_ENGLISH_US)

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(selLang)

        if self.locale.IsOk():
            self.locale.AddCatalog(__packagename__)
        else:
            self.locale = None


def main():
    """The real main. Creates and calls the main app windows. """
    youtubedl_path = Path(opt_manager.options.get("youtubedl_path", ".")).joinpath(
        YOUTUBEDL_BIN
    )

    app = BaseApp(redirect=False)
    frame = MainFrame(opt_manager, log_manager)
    frame.Show()

    if opt_manager.options.get("disable_update", False) and not youtubedl_path.exists():
        wx.MessageBox(
            _("Failed to locate youtube-dl and updates are disabled"),
            _("Error"),
            wx.OK | wx.ICON_ERROR,
        )
        frame.close()

    app.MainLoop()
