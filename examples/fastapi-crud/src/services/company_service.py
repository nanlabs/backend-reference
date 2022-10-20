from typing import List
from uuid import uuid4

from repositories.company_repository import CompanyRepository
from sqlalchemy.orm import Session

from factories.companies_factory import CompanyFactory
from models.models import Company
from models.schemas.company import NewCompanySchema, PatchCompanySchema


class CompanyService:

    @staticmethod
    async def bulk_creator(quantity: int, db: Session) -> List[Company]:
        """Creates n new mock companies"""
        factory = CompanyFactory()
        return await factory.bulk_creator(quantity, db)

    @staticmethod
    async def get_all(db: Session) -> List[Company]:
        return await CompanyRepository.get_all(db)

    @staticmethod
    async def get_by_id(id: str, db: Session) -> Company:
        return await CompanyRepository.get_by_id(id, db)

    @staticmethod
    async def patch(id: str, request: PatchCompanySchema, db: Session) -> Company:
        company: Company = await CompanyRepository.get_by_id(id, db)
        for (key, value) in request.dict().items():
            if value is not None:
                setattr(company, key, value)
        await CompanyRepository.patch(company, db)
        return company

    @staticmethod
    async def create(request: NewCompanySchema, db: Session) -> Company:
        req = request.dict()
        req["id"] = str(uuid4())
        company = Company(**req)
        await CompanyRepository.create(company, db)
        return company

    @staticmethod
    async def delete_company(id: str, db: Session) -> None:
        await CompanyRepository.delete(id, db)
