from sqlalchemy import Column, ForeignKey, Integer, String, Table

from .database import Base

movie_genres_table = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", String, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

track_songs_table = Table(
    "track_songs",
    Base.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
)