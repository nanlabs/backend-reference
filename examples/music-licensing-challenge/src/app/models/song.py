from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .associations import track_songs_table
from .database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    artist = Column(String, nullable=True)
    license_status_id = Column(
        Integer, ForeignKey("license_statuses.id"), nullable=False
    )

    tracks = relationship("Track", secondary=track_songs_table, back_populates="songs")
    license_status = relationship("LicenseStatus", back_populates="songs")
