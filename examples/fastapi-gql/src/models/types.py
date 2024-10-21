from typing import List, Optional
from uuid import UUID

import strawberry

# Types


@strawberry.type
class CompanySchema:
    company_name: str
    address: Optional[str] = strawberry.UNSET
    city: Optional[str] = strawberry.UNSET
    country: Optional[str] = strawberry.UNSET
    zip_code: Optional[str] = strawberry.UNSET
    time_zone: Optional[str] = strawberry.UNSET
    owner_name: Optional[str] = strawberry.UNSET
    owner_last_name: Optional[str] = strawberry.UNSET
    email: Optional[str] = strawberry.UNSET
    phone_number: Optional[str] = strawberry.UNSET
    tax_id: Optional[str] = strawberry.UNSET


@strawberry.type
class CompanyResponse(CompanySchema):
    id: UUID = "1"


@strawberry.type
class CompaniesResponseList:
    companies: List["CompanyResponse"]


# Messages


@strawberry.type
class CompanyNotExist:
    message: str = "No companies with that name were found. "


@strawberry.type
class CompanyListError:
    message: str = "There were some problems when querying companies. "


@strawberry.type
class GetCompanyError:
    message: str = "There were some problems when querying the company. "
