from typing import List

import strawberry

from ...models.scene import Scene as SceneModel
from .track import Track

@strawberry.type
class Scene:
    id: str
    movie_id: str
    scene_number: int
    description: str
    tracks: List[Track]

    @classmethod
    def from_model(cls, model: SceneModel) -> "Scene":
        return cls(
            id=model.id,
            movie_id=model.movie_id,
            scene_number=model.scene_number,
            description=model.description,
            tracks=[Track.from_model(t) for t in model.tracks],
        )
