from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload, selectinload

from ..models.movie import Movie
from ..models.scene import Scene
from ..models.track import Track


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_movies_with_details(self) -> List[Movie]:
        """
        Retrieves all movies with their associated genres, scenes, tracks, and songs.
        """
        result = self.db.execute(
            select(Movie).options(
                joinedload(Movie.genres),
                selectinload(Movie.scenes)
                .subqueryload(Scene.tracks)
                .subqueryload(Track.songs),
            )
        )
        return result.unique().scalars().all()

    def get_movie_by_id_with_details(self, movie_id: str) -> Movie | None:
        """
        Retrieves a specific movie by ID with all its associated details.
        """
        result = self.db.execute(
            select(Movie)
            .where(Movie.id == movie_id)
            .options(
                joinedload(Movie.genres),
                selectinload(Movie.scenes)
                .subqueryload(Scene.tracks)
                .subqueryload(Track.songs),
            )
        )
        return result.unique().scalar_one_or_none()
