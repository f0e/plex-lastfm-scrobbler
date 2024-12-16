# main.py
import logging
import time

from .clients.lastfm import LastFMScrobbler
from .config import Config
from .sources.plex import PlexTrackFetcher

logger = logging.getLogger(__name__)

MAIN_UPDATE_GAP_SECS = 1


def main():
    config = Config()

    if not config.validate():
        return

    plex = PlexTrackFetcher(server_url=Config.PLEX_SERVER_URL, token=Config.PLEX_TOKEN)

    lastfm = LastFMScrobbler(
        api_key=Config.LASTFM_API_KEY,
        api_secret=Config.LASTFM_API_SECRET,
        username=Config.LASTFM_USERNAME,
        password=Config.LASTFM_PASSWORD,
    )

    while True:
        try:
            tracks = plex.get_currently_playing(
                [library.strip() for library in Config.PLEX_LIBRARIES.split(",")]
            )

            track = (
                tracks[0] if len(tracks) > 0 else None
            )  # todo: any point supporting more than one song at once?

            lastfm.update_now_playing(track)

            if track:
                lastfm.update_track(track)

            time.sleep(MAIN_UPDATE_GAP_SECS)
        except Exception as e:
            logger.exception(e)
            time.sleep(3)


if __name__ == "__main__":
    main()
