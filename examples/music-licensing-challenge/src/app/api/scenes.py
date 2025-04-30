from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.database import get_db
from ..models.scene import Scene
from ..schemas.scenes import SceneWithAllData
from ..repository.scenes import SceneRepository

router = APIRouter()


@router.get("/", response_model=List[SceneWithAllData] | SceneWithAllData)
def read_scenes(
    id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if id is None:
        scenes = SceneRepository(db)
        return scenes.get_all_scenes_with_details()
    else:
        scene = db.query(Scene).filter(Scene.id == id).first()
        if scene is None:
            raise HTTPException(status_code=404, detail="Scene not found")
        return scene
