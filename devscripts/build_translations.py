"""Compile the application's gettext catalogs."""

import glob
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATTERN = "youtube_dl_gui/locale/*/LC_MESSAGES/youtube_dl_gui.po"


def build_translations():
    """Compile every source catalog into its corresponding MO file."""
    import polib

    for source_name in glob.glob(str(PROJECT_ROOT / CATALOG_PATTERN)):
        source = Path(source_name)
        destination = source.with_suffix(".mo")
        LOGGER.info("Building MO file for '%s'", source)
        polib.pofile(source).save_as_mofile(destination)


def main():
    """Run the translation build from the command line."""
    logging.basicConfig(level=logging.INFO)
    build_translations()


if __name__ == "__main__":
    main()
