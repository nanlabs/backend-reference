from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .associations import movie_genres_table
from .database import Base


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    movies = relationship(
        "Movie", secondary=movie_genres_table, back_populates="genres"
    )
