import strawberry
from models import types
from services.company_service import CompanyService

company_service = CompanyService()


CompaniesQueryResponse = strawberry.union(
    "CompaniesQueryResponse", types=(types.CompaniesResponseList, types.CompanyListError)
)
CompanyQueryResponse = strawberry.union(
    "CompanyQueryResponse", types=(types.CompanyResponse, types.GetCompanyError)
)


@strawberry.type
class Query:

    @strawberry.field
    def get_companies(self) -> CompaniesQueryResponse:
        result = company_service.get_all_companies()
        if not result:
            return types.CompanyListError
        if isinstance(result, str):
            types.CompanyListError.message += result
            return types.CompanyListError
        return types.CompaniesResponseList(companies=result)

    @strawberry.field
    def company(self) -> CompanyQueryResponse:
        result = company_service.get_company()
        if not result:
            return types.GetCompanyError
        if isinstance(result, str):
            types.GetCompanyError.message += result
            return types.GetCompanyError
        return types.CompanyResponse(**result.__dict__)
