# main.py
import logging
import time

import requests

from .clients.lastfm import LastFMScrobbler
from .config import Config
from .sources.plex import PlexTrackFetcher

logger = logging.getLogger(__name__)

MAIN_UPDATE_GAP_SECS = 1


def main():
    config = Config()

    if not config.validate():
        return

    while True:
        lastfm = connect_lastfm(config)
        if not lastfm:
            time.sleep(15)
            continue

        plex = connect_plex(config)
        if not plex:
            time.sleep(15)
            continue

        logger.info("Connected, listening for scrobbles.")
        song_loop(config, plex, lastfm)


def connect_lastfm(config):
    try:
        return LastFMScrobbler(
            api_key=config.LASTFM_API_KEY,
            api_secret=config.LASTFM_API_SECRET,
            username=config.LASTFM_USERNAME,
            password=config.LASTFM_PASSWORD,
        )
    except Exception as e:
        logger.error(e)
        logger.error("Failed to connect to Last.fm")
        return None


def connect_plex(config):
    try:
        return PlexTrackFetcher(
            server_url=config.PLEX_SERVER_URL, token=config.PLEX_TOKEN
        )
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
        logger.error(f"Failed to connect to Plex server at {config.PLEX_SERVER_URL}")
        return None


def song_loop(config, plex, lastfm):
    while True:
        try:
            process_tracks(config, plex, lastfm)

            time.sleep(MAIN_UPDATE_GAP_SECS)
        except requests.exceptions.ConnectionError as e:
            logger.error(e)
            logger.error("Lost connection to Plex")
            break
        except Exception as e:
            logger.exception(e)
            time.sleep(3)


def process_tracks(config, plex, lastfm):
    tracks = plex.get_currently_playing(
        [library.strip() for library in config.PLEX_LIBRARIES.split(",")]
    )

    track = (
        tracks[0] if tracks else None
    )  # todo: any point supporting more than one song at once?

    lastfm.update_now_playing(track)

    if track:
        lastfm.update_track(track)


if __name__ == "__main__":
    main()
