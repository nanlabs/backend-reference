from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .associations import movie_genres_table
from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    director = Column(String, nullable=True)
    description = Column(String, nullable=True)
    poster = Column(String, nullable=True)

    genres = relationship(
        "Genre", secondary=movie_genres_table, back_populates="movies"
    )
    scenes = relationship("Scene", back_populates="movie", cascade="all, delete-orphan")
