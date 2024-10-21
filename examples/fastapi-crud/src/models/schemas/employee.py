from pydantic import BaseModel, EmailStr, HttpUrl


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

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


class NewEmployeeSchema(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    state_province: str
    country: str
    zip_code: str | None
    time_zone: str | None
    personal_id: str
    email: EmailStr
    phone_number: str
    company: str | None
    role: str
    avatar_url: HttpUrl | None

    class Config:
        """This config validates the request, if it has extra fields raises a validation error
        https://pydantic-docs.helpmanual.io/usage/model_config/#options
        """

        extra = "forbid"


class PatchEmployeeSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    address: str | None
    city: str | None
    state_province: str | None
    country: str | None
    zip_code: str | None
    time_zone: str | None
    personal_id: str | None
    email: EmailStr | None
    phone_number: str | None
    is_manager: bool | None
    company: str | None
    role: str | None
    avatar_url: HttpUrl | None

    class Config:
        """This config validates the request, if it has extra fields raises a validation error
        https://pydantic-docs.helpmanual.io/usage/model_config/#options
        """

        extra = "forbid"
