"""
This will generate the .pot and .mo files for the application domain and
languages defined below.

The .po and .mo files are placed as per convention in

"__packagename__/locale/lang/LC_MESSAGES"

The .pot file is placed in the locale folder.

This script or something similar should be added to your build process.

The actual translation work is normally done using a tool like poEdit or
similar, it allows you to generate a particular language catalog from the .pot
file or to use the .pot to merge new translations into an existing language
catalog.

"""


import subprocess
import sys
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
gtOptions = f"-a -d {langDomain} -o {langDomain}.pot -p {outFolder} {appFolder}"
tCmd = f"{pyExe} {pyGettext} {gtOptions}"

print("Generating the .pot file")
print(f"cmd: {tCmd}")
rCode = subprocess.call(tCmd)

if rCode != 0:
    sys.exit(f"return code: {rCode}")

print("")

for tLang in supportedLang:
    # build command for msgfmt
    langDir = appFolder.joinpath(f"locale/{tLang}/LC_MESSAGES")
    poFile = langDir.joinpath(langDomain).with_suffix(".po")
    tCmd = f"{pyExe} {pyMsgfmt} {poFile}"

    print("Generating the .mo file")
    print(f"cmd: {tCmd}")
    rCode = subprocess.call(tCmd)
    if rCode != 0:
        sys.exit(f"return code: {rCode}")
