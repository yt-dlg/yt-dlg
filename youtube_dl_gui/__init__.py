import os

from .info import (
    __appname__,
    __author__,
    __contact__,
    __description__,
    __descriptionfull__,
    __githuburl__,
    __license__,
    __licensefull__,
    __maintainer__,
    __mcontact__,
    __packagename__,
    __projecturl__,
)
from .version import __version__

if os.environ.get("WAYLAND_DISPLAY"):
    os.environ["GDK_BACKEND"] = "x11"

if not os.path.exists(os.environ.get("SSL_CERT_DIR", "")):
    os.environ["SSL_CERT_DIR"] = "/etc/ssl/certs"
