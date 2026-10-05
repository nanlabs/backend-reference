from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


class EmployeeSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    address: str
    city: str
    state_province: str
    country: str
    zip_code: str
    time_zone: str
    personal_id: str
    email: EmailStr
    phone_number: str
    is_manager: bool
    company: str
    role: str
    avatar_url: HttpUrl

    model_config = ConfigDict(from_attributes=True)


class ShortEmployeeSchema(BaseModel):
    id: str
    company: str
    first_name: str
    last_name: str
    country: str
    email: EmailStr
    phone_number: str
    is_manager: bool
    role: str
    avatar_url: HttpUrl

    model_config = ConfigDict(from_attributes=True)


class NewEmployeeSchema(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    state_province: str
    country: str
    zip_code: str
    time_zone: str | None = None
    personal_id: str
    email: EmailStr
    phone_number: str
    company: str | None = None
    role: str
    avatar_url: HttpUrl | None = None

    model_config = ConfigDict(extra="forbid")


class PatchEmployeeSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    city: str | None = None
    state_province: str | None = None
    country: str | None = None
    zip_code: str | None = None
    time_zone: str | None = None
    personal_id: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    is_manager: bool | None = None
    company: str | None = None
    role: str | None = None
    avatar_url: HttpUrl | None = None

    model_config = ConfigDict(extra="forbid")
