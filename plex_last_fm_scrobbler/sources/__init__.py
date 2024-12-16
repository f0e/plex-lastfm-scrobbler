from dataclasses import dataclass


@dataclass
class Track:
    name: str
    artist: str
    album: str | None = None
    progress_ms: float | None = None
    duration_ms: float | None = None
