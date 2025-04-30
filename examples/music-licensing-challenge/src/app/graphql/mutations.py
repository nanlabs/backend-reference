from typing import Optional

from sqlalchemy.orm import Session
from strawberry import ID, mutation, type

from ..db.database import get_db
from ..repository.songs import SongRepository
from ..schemas.songs import LicenseStatusEnum
from .pubsub import trigger_license_change_subscription
from .types.song import Song


@type
class Mutations:
    @mutation
    async def update_song(
        self,
        id: ID,
        license_status: Optional[LicenseStatusEnum] = None,
    ) -> Optional[Song]:
        db: Session = get_db()
        song_repository = SongRepository(db)
        song = song_repository.update_song(id, license_status)
        if song is None:
            return None
        if license_status:
            await trigger_license_change_subscription(song)
        return Song.from_model(song)
