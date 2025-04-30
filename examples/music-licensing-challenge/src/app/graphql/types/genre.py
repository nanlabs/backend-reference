import strawberry

from ...models.genre import Genre as GenreModel


@strawberry.type
class Genre:
    id: int
    name: str

    @classmethod
    def from_model(cls, model: GenreModel) -> "Genre":
        return cls(
            id=model.id,
            name=model.name,
        )
