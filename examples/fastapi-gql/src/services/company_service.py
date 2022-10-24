from factories.company_factory import CompanyFactory


class CompanyService:

    def get_company(self):
        return CompanyFactory()

    def get_all_companies(self):
        return [CompanyFactory() for _ in range(10)]
