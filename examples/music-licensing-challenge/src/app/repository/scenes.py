from typing import List

from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload

from ..models.scene import Scene
from ..models.track import Track


class SceneRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_scenes_with_details(self) -> List[Scene]:
        result = self.db.execute(
            select(Scene).options(
                selectinload(Scene.tracks).subqueryload(Track.songs),
            )
        )
        return result.unique().scalars().all()

    def get_scene_by_id_with_details(self, scene_id: str) -> Scene | None:
        result = self.db.execute(
            select(Scene)
            .where(Scene.id == scene_id)
            .options(
                selectinload(Scene.tracks).subqueryload(Track.songs),
            )
        )
        return result.unique().scalar_one_or_none()
