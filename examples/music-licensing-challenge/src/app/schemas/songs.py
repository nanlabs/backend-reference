import enum
from typing import Optional

import strawberry
from pydantic import BaseModel, ConfigDict, Field


@strawberry.enum
class LicenseStatusEnum(enum.Enum):
    NOT_LICENSED = "NOT_LICENSED"
    PENDING = "PENDING"
    LICENSED = "LICENSED"


class LicenseStatus(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
    id: int = Field(...)
    name: str = Field(...)


class Song(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: int = Field(...)
    title: str = Field(...)
    artist: Optional[str] = Field(None)
    license_status: Optional[LicenseStatus] = Field(
        None,
        alias="licenseStatus",
    )
