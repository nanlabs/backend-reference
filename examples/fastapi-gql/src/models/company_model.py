
from typing import Optional
from uuid import UUID, uuid4

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Company(models.Model):
    id: Optional[UUID] = fields.UUIDField(pk=True, default=uuid4)
    company_name: str = fields.CharField(max_length=100, unique=True)
    address: Optional[str] = fields.CharField(max_length=100, null=True)
    city: Optional[str] = fields.CharField(max_length=100, null=True)
    country: Optional[str] = fields.CharField(max_length=100, null=True)
    zip_code: Optional[str] = fields.CharField(max_length=100, null=True)
    time_zone: Optional[str] = fields.CharField(max_length=20, null=True)
    owner_name: Optional[str] = fields.CharField(max_length=100, null=True)
    owner_last_name: Optional[str] = fields.CharField(max_length=100, null=True)
    email: Optional[str] = fields.CharField(max_length=100, null=True)
    phone_number: Optional[str] = fields.CharField(max_length=100, null=True)
    tax_id: Optional[str] = fields.CharField(max_length=100, null=True)

    class PydanticMeta:
        exclude = ("_partial", "_saved_in_db", "_custom_generated_pk")


Company_Pydantic = pydantic_model_creator(Company, name="Company")
