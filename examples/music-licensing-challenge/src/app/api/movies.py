from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.database import get_db
from ..models.movie import Movie
from ..schemas.movies import MovieWithAllData
from ..repository.movies import MovieRepository

router = APIRouter()


@router.get("/", response_model=List[MovieWithAllData] | MovieWithAllData)
def read_movies(
    id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if id is None:
        movies = MovieRepository(db)
        return movies.get_all_movies_with_details()
    else:
        movie = db.query(Movie).filter(Movie.id == id).first()
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
