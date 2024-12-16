from .sources import Track


def is_same_track(track1: Track | None, track2: Track | None) -> bool:
    if not track1 and not track2:
        return True

    if not track1 or not track2:
        return False

    return (
        track1.name == track2.name
        and track1.artist == track2.artist
        and track1.album == track2.album
    )
