from typing import Any

from app.constants import DESC
from app.schemas.sorting import Sorting


def multisort(objects: list[Any], sorting: Sorting) -> list[Any]:
    sort_by = sorting.sort_by or []
    sort_order = sorting.sort_order or []

    def sort_key(obj: list[Any]) -> tuple[Any]:
        keys = []
        for attr, order in zip(sort_by, sort_order):
            value = getattr(obj, attr)
            if order == DESC:
                if isinstance(value, (int, float)):
                    value = -value
                elif isinstance(value, str):
                    value = "".join(chr(255 - ord(char)) for char in value)
            keys.append(value)
        return tuple(keys)

    objects.sort(key=sort_key)
    return objects
