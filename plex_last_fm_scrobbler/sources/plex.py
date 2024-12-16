# plex_client.py
import logging

from plexapi.audio import Album, Artist
from plexapi.audio import Track as PlexTrack
from plexapi.server import PlexServer

from . import Track

logger = logging.getLogger(__name__)


class PlexTrackFetcher:
    def __init__(self, server_url: str, token: str):
        self.client = PlexServer(server_url, token)

    def get_currently_playing(self, libraries: list[str]) -> list[Track]:
        if len(libraries) == 0:
            logger.warning("No libraries selected! No tracks will be scrobbled.")
            return []

        tracks = []

        for session in self.client.sessions():
            # Filter for audio tracks that are currently playing
            if (
                session.type != "track"
                or session.player.state != "playing"
                or session.librarySectionTitle not in libraries
            ):
                continue

            track: PlexTrack = session
            artist: Artist = track.artist()
            album: Album = track.album()

            tracks.append(
                Track(
                    name=track.title,
                    artist=artist.title,
                    album=album.title,
                    progress_ms=track.viewOffset,
                    duration_ms=track.duration,
                )
            )

        return tracks
