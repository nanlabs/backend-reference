from uuid import UUID

FiltersTypes = str | list[str] | int | float | bool | UUID | list[UUID]
FiltersData = dict[str, FiltersTypes]
