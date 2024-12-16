import logging

from rich.logging import RichHandler

PROJECT_URL = "https://github.com/f0e/plex-last-fm-scrobbler"
APP_NAME = "plex-last-fm-scrobbler"

FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True),
    ],
)

logger = logging.getLogger(__name__)
