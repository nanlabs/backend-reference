from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .songs import Song


class Track(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: int = Field(...)
    track_type: Optional[str] = Field(
        None,
        alias="trackType",
    )
    songs: List[Song] = Field(...)


class Scene(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: int = Field(...)
    scene_number: int = Field(
        ...,
        alias="sceneNumber",
    )
    description: Optional[str] = Field(None)
    tracks: List[Track] = Field(...)


class SceneBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    scene_number: int = Field(..., alias="sceneNumber")
    movie_id: str = Field(..., alias="movieId")
    description: Optional[str] = Field(None)


class SceneWithAllData(SceneBase):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: int = Field(...)
    tracks: List[Track] = Field(...)
