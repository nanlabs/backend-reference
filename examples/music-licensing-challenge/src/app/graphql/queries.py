from typing import List, Optional

from strawberry import ID, field, type

from ..db.database import get_db
from ..repository.licenses import LicenseRepository
from ..repository.movies import MovieRepository
from ..repository.scenes import SceneRepository
from ..repository.songs import SongRepository
from .types.movie import Movie
from .types.scene import Scene
from .types.song import Song
from .types.song import LicenseStatus


@type
class Query:
    @field
    def all_movies(self) -> List[Movie]:
        db = get_db()
        movies = MovieRepository(db).get_all_movies_with_details()
        return [Movie.from_model(m) for m in movies]

    @field
    def movie(self, id: ID) -> Optional[Movie]:
        db = get_db()
        movie = MovieRepository(db).get_movie_by_id_with_details(id)
        return Movie.from_model(movie) if movie else None

    @field
    def scene(self, id: ID) -> Optional[Scene]:
        db = get_db()
        scene = SceneRepository(db).get_scene_by_id_with_details(id)
        return Scene.from_model(scene) if scene else None

    @field
    def all_scenes(self) -> List[Scene]:
        db = get_db()
        scenes = SceneRepository(db).get_all_scenes_with_details()
        return [Scene.from_model(s) for s in scenes]

    @field
    def all_license_status(self) -> List[LicenseStatus]:
        db = get_db()
        licenses = LicenseRepository(db).get_all_licenses()
        return [LicenseStatus.from_model(s) for s in licenses]
    
    @field
    def song(self, id: ID) -> Optional[Song]:
        db = get_db()
        song = SongRepository(db).get_song_by_id(id)
        return Song.from_model(song) if song else None