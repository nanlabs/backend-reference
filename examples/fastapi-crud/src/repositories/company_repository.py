import logging
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from exceptions.database_exceptions import DatabaseExceptions
from models.models import Company

logger = logging.getLogger(__name__)


class CompanyRepository:
    @staticmethod
    async def get_all(db: Session) -> List[Company]:
        """Gets all company's records from the DB"""
        try:
            return db.query(Company).all()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error(e)

    @staticmethod
    async def get_by_id(id: str, db: Session) -> Company:
        """Gets a single company's records from the DB by id"""
        try:
            company = db.query(Company).filter(Company.id == id).first()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error(e)

        if not company:
            logger.error(f"The company_id: {id} does not exist")
            DatabaseExceptions.throw_not_found_error("Company")
        return company

    @staticmethod
    async def create(company: Company, db: Session) -> None:
        """Creates a company record on the DB"""
        try:
            db.add(company)
            db.commit()
            db.refresh(company)
        except IntegrityError as integrity_error:
            logger.error(integrity_error, exc_info=True)
            DatabaseExceptions.throw_db_integrity_error(integrity_error)
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error()

    @staticmethod
    async def delete(id: str, db: Session) -> None:
        """Deletes a company record from DB"""
        company = await CompanyRepository.get_by_id(id, db)
        try:
            db.delete(company)
            db.commit()
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error()

    @staticmethod
    async def patch(company: Company, db: Session):
        """Updates a company record in DB"""
        try:
            db.add(company)
            db.commit()
        except IntegrityError as integrity_error:
            logger.error(integrity_error, exc_info=True)
            DatabaseExceptions.throw_db_integrity_error(integrity_error)
        except Exception as e:
            logger.error(e, exc_info=True)
            DatabaseExceptions.throw_internal_server_error(e)
