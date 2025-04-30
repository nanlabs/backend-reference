from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .scenes import Scene


class Genre(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: int = Field(...)
    name: str = Field(...)


class MovieBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    title: str = Field(...)
    year: int = Field(...)
    director: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    poster: Optional[str] = Field(None)


class MovieWithAllData(MovieBase):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: str = Field(...)
    genres: List[Genre] = Field(...)
    scenes: List[Scene] = Field(...)
