# -*- coding: utf-8 -*-
"""
This will generate the .pot and .mo files for the application domain and
languages defined below.

The .po and .mo files are placed as per convention in

"appfolder/locale/lang/LC_MESSAGES"

The .pot file is placed in the locale folder.

This script or something similar should be added to your build process.

The actual translation work is normally done using a tool like poEdit or
similar, it allows you to generate a particular language catalog from the .pot
file or to use the .pot to merge new translations into an existing language
catalog.

"""


import os
import sys
import subprocess
from pathlib import Path

import wx


__packagename__ = "youtube_dl_gui"

# language domain
langDomain = __packagename__
# languages you want to support
supLang = {
    "en_US": wx.LANGUAGE_ENGLISH,
    "es_CU": wx.LANGUAGE_SPANISH,
}

# we remove English as source code strings are in English
supportedLang = [lang for lang in supLang if lang != "en_US"]

PATH = Path(__file__).resolve().parent
appFolder = PATH.parent.joinpath(__packagename__)

# setup some stuff to get at Python I18N tools/utilities

pyPath = Path(sys.executable).resolve()
pyExe = pyPath.name
pyFolder = pyPath.parent
pyToolsFolder = pyFolder.joinpath("Tools")
pyI18nFolder = pyToolsFolder.joinpath("i18n")
pyGettext = pyI18nFolder.joinpath("pygettext.py")
pyMsgfmt = pyI18nFolder.joinpath("msgfmt.py")
outFolder = appFolder.joinpath("locale")

# build command for pygettext
gtOptions = "-a -d %s -o %s.pot -p %s %s"
tCmd = (
    pyExe
    + " "
    + str(pyGettext)
    + " "
    + (gtOptions % (langDomain, langDomain, outFolder, appFolder))
)
print("Generating the .pot file")
print("cmd: %s" % tCmd)
rCode = subprocess.call(tCmd)
print("return code: %s\n\n" % rCode)

for tLang in supportedLang:
    # build command for msgfmt
    langDir = appFolder.joinpath("locale/%s/LC_MESSAGES" % tLang)
    poFile = langDir.joinpath(langDomain).with_suffix(".po")
    tCmd = pyExe + " " + str(pyMsgfmt) + " " + str(poFile)

    print("Generating the .mo file")
    print("cmd: %s" % tCmd)
    rCode = subprocess.call(tCmd)
    print("return code: %s\n\n" % rCode)
