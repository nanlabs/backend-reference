from typing import Any

from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    description: str
    summary: Any
    media_url: str
    preview_image_url: str
    owner_id: str


class NoteCreate(NoteBase):
    id: str

class NoteUpdate(NoteBase):
    id: str

class NoteOut(NoteBase):
    class Config:
        from_attributes = True
