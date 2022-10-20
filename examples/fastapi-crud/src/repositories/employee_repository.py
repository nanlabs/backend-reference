import logging
from typing import List

from repositories.company_repository import CompanyRepository
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from exceptions.database_exceptions import DatabaseExceptions
from models.models import Employee

logger = logging.getLogger(__name__)


class EmployeeRepository:

    @staticmethod
    async def get_all(db: Session) -> List[Employee]:
        try:
            return db.query(Employee).all()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error(e)

    @staticmethod
    async def get_all_for_company(company_id: str, db: Session):
        await CompanyRepository.get_by_id(company_id, db)
        try:
            return db.query(Employee).filter(Employee.company == company_id).all()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error(e)

    @staticmethod
    async def get_by_id(id: str, db: Session) -> Employee:
        try:
            employee = db.query(Employee).filter(Employee.id == id).first()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error(e)
        if not employee:
            logger.error(f"The employee_id: {id} does not exist")
            DatabaseExceptions.throw_not_found_error("Employee")
        return employee

    @staticmethod
    async def create(employee: Employee, db: Session):
        try:
            db.add(employee)
            db.commit()
            db.refresh(employee)
        except IntegrityError as integrity_error:
            logger.error(integrity_error, exc_info=True)
            DatabaseExceptions.throw_db_integrity_error(integrity_error)
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error()

    @staticmethod
    async def delete(id: str, db: Session) -> None:
        """Deletes an employee record from DB"""
        company = await EmployeeRepository.get_by_id(id, db)
        try:
            db.delete(company)
            db.commit()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error()

    @staticmethod
    async def patch(employee: Employee, db: Session):
        """Updates a company record in DB"""
        try:
            db.add(employee)
            db.commit()
        except IntegrityError as integrity_error:
            logger.error(integrity_error, exc_info=True)
            DatabaseExceptions.throw_db_integrity_error(integrity_error)
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error()
