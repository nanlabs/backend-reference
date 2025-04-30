from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    scene_number = Column(Integer)
    description = Column(String, nullable=True)

    movie = relationship("Movie", back_populates="scenes")
    tracks = relationship("Track", back_populates="scene", cascade="all, delete-orphan")
