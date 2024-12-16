import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    # plex configuration
    PLEX_SERVER_URL = os.getenv("PLEX_SERVER_URL", "")
    PLEX_TOKEN = os.getenv("PLEX_TOKEN", "")
    PLEX_LIBRARIES = os.getenv("PLEX_LIBRARIES", "")

    # last.fm configuration
    LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")
    LASTFM_API_SECRET = os.getenv("LASTFM_API_SECRET", "")
    LASTFM_USERNAME = os.getenv("LASTFM_USERNAME", "")
    LASTFM_PASSWORD = os.getenv("LASTFM_PASSWORD", "")

    @classmethod
    def validate(cls):
        missing_configs = []

        # check plex configuration
        if cls.PLEX_SERVER_URL == "":
            missing_configs.append("PLEX_SERVER_URL (Plex server address)")
        if cls.PLEX_LIBRARIES == "":
            missing_configs.append("PLEX_LIBRARIES (Plex libraries to scrobble)")
        if cls.PLEX_TOKEN == "":
            missing_configs.append("PLEX_TOKEN (Plex authentication token)")

        # check last.fm configuration
        if cls.LASTFM_API_KEY == "":
            missing_configs.append("LASTFM_API_KEY (Last.fm API key)")
        if cls.LASTFM_API_SECRET == "":
            missing_configs.append("LASTFM_API_SECRET (Last.fm API secret)")
        if cls.LASTFM_USERNAME == "":
            missing_configs.append("LASTFM_USERNAME (Last.fm username)")
        if cls.LASTFM_PASSWORD == "":
            missing_configs.append("LASTFM_PASSWORD (Last.fm password)")

        # log missing configuration items
        if missing_configs:
            logger.error("Missing configuration variables:")
            for config in missing_configs:
                logger.error(f"- {config}")
            return False

        return True
