from typing import List

import strawberry

from ...models.movie import Movie as MovieModel
from .genre import Genre
from .scene import Scene


@strawberry.type
class Movie:
    id: str
    title: str
    year: int
    director: str
    description: str
    poster: str
    genres: List[Genre]
    scenes: List[Scene]

    @classmethod
    def from_model(cls, model: MovieModel) -> "Movie":
        return cls(
            id=model.id,
            title=model.title,
            year=model.year,
            director=model.director,
            description=model.description,
            poster=model.poster,
            genres=[Genre.from_model(g) for g in model.genres],
            scenes=[Scene.from_model(s) for s in model.scenes],
        )
