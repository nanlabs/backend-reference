from typing import Optional

from sqlalchemy.orm import Session

from ..models.licenses import LicenseStatus
from ..models.song import Song
from ..schemas.songs import LicenseStatusEnum


class SongRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_song_by_id(self, song_id: str) -> Optional[Song]:
        return self.db.query(Song).filter(Song.id == song_id).first()

    def update_song(
        self,
        song_id: str,
        license_status: Optional[LicenseStatusEnum],
    ) -> Optional[Song]:
        song = self.get_song_by_id(song_id)
        if song:
            if license_status is not None:
                db_license_status = (
                    self.db.query(LicenseStatus)
                    .filter(LicenseStatus.name == license_status.value)
                    .first()
                )
                if db_license_status:
                    song.license_status = db_license_status
                else:
                    print(
                        f"Warning: License status '{license_status.value}' not found in database."
                    )
                    return None

            self.db.commit()
            self.db.refresh(song)
            return song
        return None
