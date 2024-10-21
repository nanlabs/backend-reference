from uuid import UUID

from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteOut
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{note_id}", response_model=NoteOut, operation_id="get_note")
def get_note(
    note_id: UUID,
) -> NoteOut:
    repository = NoteRepository()
    try:
        note = repository.get_note_by_id(note_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Note not found.") from e
    return note


@router.get("/", response_model=list[NoteOut], operation_id="get_all_notes")
def get_all_notes() -> list[NoteOut]:
    repository = NoteRepository()
    return repository.get_all_notes()
