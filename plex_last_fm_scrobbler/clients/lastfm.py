import logging
import time

import pylast

from ..sources.plex import Track
from ..utils import is_same_track

logger = logging.getLogger(__name__)


class LastFMScrobbler:
    current_track: Track | None = None
    to_scrobble_track: bool = False
    now_playing_track: Track | None = None
    played_amount: float = 0
    last_progress_ms: float | None = None

    def __init__(self, api_key: str, api_secret: str, username: str, password: str):
        self.network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret,
            username=username,
            password_hash=pylast.md5(password),
        )
        self.current_track = None
        self.to_scrobble_track = False
        self.now_playing_track = None

        self.played_amount = 0
        self.last_progress_ms = None

    def update_now_playing(self, track: Track | None):
        try:
            # check if this is a new track
            if track and not is_same_track(track, self.current_track):
                # scrobble track if queued
                if self.to_scrobble_track and self.current_track:
                    self._scrobble_track(self.current_track)
                    self.to_scrobble_track = False

                # update current track
                self.current_track = track
                self.played_amount = 0
                self.last_progress_ms = None

                logger.info(f"Now playing: {track.artist} - {track.name}")

            # Update now playing
            if not is_same_track(self.now_playing_track, track):
                if track:
                    self.network.update_now_playing(
                        artist=track.artist if track else None,
                        title=track.name if track else None,
                        album=track.album if track else None,
                    )
                else:
                    pass
                    # # TODO: FIX. HOW DO YOU RESET THE NOW PLAYING????
                    # self.network.update_now_playing(
                    #     artist=self.current_track.artist,
                    #     title=self.current_track.name,
                    #     album=self.current_track.album,
                    # )

                self.now_playing_track = track
                logger.info("updated now playing track")
        except Exception as e:
            logger.exception(e)

    def should_scrobble(self, track: Track) -> bool:
        if self.to_scrobble_track:
            return False

        # https://www.last.fm/api/scrobbling#scrobble-requests
        MIN_TRACK_DURATION_MS = 30 * 1000  # 30 seconds
        MIN_TRACK_PROGRESS_MS = 4 * 60 * 1000  # 4 minutes
        MIN_TRACK_PROGRESS_PERCENT = 0.5

        if not track.duration_ms or track.duration_ms < MIN_TRACK_DURATION_MS:
            return False

        return (
            self.played_amount / track.duration_ms >= MIN_TRACK_PROGRESS_PERCENT
            or self.played_amount > MIN_TRACK_PROGRESS_MS
        )

    def update_track(self, track: Track):
        if (
            self.last_progress_ms is not None
            and track.progress_ms is not None
            and track.progress_ms != self.last_progress_ms
        ):
            new_progress = (
                track.progress_ms - self.last_progress_ms
            )  # could be negative if you seek back, but i think that's fine tbh

            self.played_amount += new_progress

            logger.debug(
                f"played {self.played_amount / 1000} secs of the song ({self.last_progress_ms} -> {track.progress_ms})"
            )
        self.last_progress_ms = track.progress_ms

        if not self.to_scrobble_track:
            self.to_scrobble_track = self.should_scrobble(track)
            if self.to_scrobble_track:
                logger.info(f"Queued scrobble for {track.artist} - {track.name}")

    def _scrobble_track(self, track: Track):
        try:
            self.network.scrobble(
                artist=track.artist,
                title=track.name,
                album=track.album,
                timestamp=int(time.time()),  # todo: scrobble start time
            )

            logger.info(f"Scrobbled: {track.artist} - {track.name}")
        except Exception as e:
            logger.error(f"Error scrobbling track: {e}")
