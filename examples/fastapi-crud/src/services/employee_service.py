from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from exceptions.database_exceptions import DatabaseExceptions
from factories.employee_factory import EmployeesFactory
from models.models import Employee
from models.schemas.employee import NewEmployeeSchema, PatchEmployeeSchema
from repositories.employee_repository import EmployeeRepository
from services.company_service import CompanyService


class EmployeeService:

    @staticmethod
    async def bulk_creator(quantity: int, db: Session, company_id: str | None) -> List[Employee]:
        factory = EmployeesFactory()
        if company_id is not None:
            await CompanyService.get_by_id(company_id, db)
            return await factory.bulk_creator_for_company(quantity, db, company_id)
        companies = await CompanyService.get_all(db)
        if len(companies) == 0:
            DatabaseExceptions.throw_not_found_error("Companies")
        return await factory.bulk_creator(quantity, db, companies)

    @staticmethod
    async def get_all(db: Session) -> List[Employee]:
        return await EmployeeRepository.get_all(db)

    @staticmethod
    async def get_all_for_company(company_id: str, db: Session) -> List[Employee]:
        return await EmployeeRepository.get_all_for_company(company_id, db)

    @staticmethod
    async def get_by_id(id: str, db: Session) -> Employee:
        employee = await EmployeeRepository.get_by_id(id, db)
        return employee

    @staticmethod
    async def create(request: NewEmployeeSchema, db: Session) -> Employee:
        req = request.dict()
        req["id"] = str(uuid4())
        req["is_manager"] = False
        employee = Employee(**req)
        await EmployeeRepository.create(employee, db)
        return employee

    @staticmethod
    async def patch(id: str, request: PatchEmployeeSchema, db: Session) -> Employee:
        employee: Employee = await EmployeeRepository.get_by_id(id, db)
        for (key, value) in request.dict().items():
            if value is not None:
                setattr(employee, key, value)
        await EmployeeRepository.patch(employee, db)
        return employee

    @staticmethod
    async def delete_employee(id: str, db: Session) -> None:
        await EmployeeRepository.delete(id, db)
