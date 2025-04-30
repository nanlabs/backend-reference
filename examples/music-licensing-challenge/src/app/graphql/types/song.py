from typing import Optional

import strawberry

from ...models.song import Song as SongModel


@strawberry.type
class LicenseStatus:
    id: int
    status: str

    @classmethod
    def from_model(cls, model):
        return cls(id=model.id, status=model.name)


@strawberry.type
class Song:
    id: str
    title: str
    artist: Optional[str]
    license_status: str

    @classmethod
    def from_model(cls, model: SongModel) -> "Song":
        return cls(
            id=model.id,
            title=model.title,
            artist=model.artist,
            license_status=model.license_status.name if model.license_status else None,
        )
