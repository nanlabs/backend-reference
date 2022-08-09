
from typing import List, Optional

from pydantic import BaseModel


class Users(BaseModel):
    id: int
    name: str
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    age: Optional[int]
    license: Optional[str]


class UsersList(BaseModel):
    __root__: List[Users]
