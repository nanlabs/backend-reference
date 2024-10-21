from uuid import UUID

from app.schemas.note import NoteBase


class NoteRepository:
    def __init__(self):
        pass

    def get_note_by_id(self, note_id: UUID) -> NoteBase:
        mock_note = NoteBase(
            id=str(note_id),
            title="Mocked Note",
            description="This is a mocked note.",
            summary="summary",
            media_url="https://localhost",
            preview_image_url="https://localhost",
            owner_id=str(UUID("12345678-1234-5678-1234-567812345678")),
            created_at="2021-01-01T00:00:00",
            updated_at="2021-01-01T00:00:00",
        )

        return mock_note

    def get_all_notes(self) -> list[NoteBase]:
        mock_note_list = [
            NoteBase(
                id=str(UUID("12345678-1234-5678-1234-567812345678")),
                title="Mocked Note",
                description="This is a mocked note.",
                summary="summary",
                media_url="https://localhost",
                preview_image_url="https://localhost",
                owner_id=str(UUID("12345678-1234-5678-1234-567812345678")),
                created_at="2021-01-01T00:00:00",
                updated_at="2021-01-01T00:00:00",
            ),
            NoteBase(
                id=str(UUID("87654321-4321-8765-4321-876543218765")),
                title="Mocked Note",
                description="This is a mocked note.",
                summary="summary",
                media_url="https://localhost",
                preview_image_url="https://localhost",
                owner_id=str(UUID("12345678-1234-5678-1234-567812345678")),
                created_at="2021-01-01T00:00:00",
                updated_at="2021-01-01T00:00:00",
            ),
        ]
        return [NoteBase.model_validate(note) for note in mock_note_list]
