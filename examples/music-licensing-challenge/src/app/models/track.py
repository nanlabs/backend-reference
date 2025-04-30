from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .associations import track_songs_table
from .database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    track_type = Column(String, nullable=True)

    scene = relationship("Scene", back_populates="tracks")
    songs = relationship("Song", secondary=track_songs_table, back_populates="tracks")
