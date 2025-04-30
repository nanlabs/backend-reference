from typing import List

import strawberry

from ...models.track import Track as TrackModel
from .song import Song


@strawberry.type
class Track:
    id: str
    track_type: str
    songs: List[Song]

    @classmethod
    def from_model(cls, model: TrackModel) -> "Track":
        return cls(
            id=model.id,
            track_type=model.track_type,
            songs=[Song.from_model(song) for song in model.songs],
        )
