from pydantic import BaseModel, ConfigDict, EmailStr


class CompanySchema(BaseModel):
    id: str
    company_name: str
    address: str
    address_line_2: str | None = None
    city: str
    state_province: str
    country: str
    zip_code: str
    time_zone: str | None = None
    owner_name: str | None = None
    owner_last_name: str | None = None
    email: EmailStr
    phone_number: str | None = None
    tax_id: str

    model_config = ConfigDict(from_attributes=True)


class NewCompanySchema(BaseModel):
    company_name: str
    address: str
    address_line_2: str | None = None
    city: str
    state_province: str
    country: str
    zip_code: str
    time_zone: str | None = None
    owner_name: str | None = None
    owner_last_name: str | None = None
    email: EmailStr
    phone_number: str | None = None
    tax_id: str

    model_config = ConfigDict(extra="forbid")


class PatchCompanySchema(BaseModel):
    company_name: str | None = None
    address: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    state_province: str | None = None
    country: str | None = None
    zip_code: str | None = None
    time_zone: str | None = None
    owner_name: str | None = None
    owner_last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    tax_id: str | None = None

    model_config = ConfigDict(extra="forbid")
