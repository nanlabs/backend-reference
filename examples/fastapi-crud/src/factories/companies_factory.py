from typing import List
from uuid import uuid4

from faker import Faker
from models.models import Company
from repositories.company_repository import CompanyRepository
from sqlalchemy.orm import Session


class CompanyFactory:
    """Generates Companies in the DB"""

    def __init__(self) -> None:
        self.companies = list()

    async def _company_creator(self, db: Session) -> None:
        """Creates a single fake company in the DB"""
        fake = Faker()
        new_company = Company(
            id=str(uuid4()),
            company_name=fake.company(),
            address=fake.street_address(),
            city=fake.city(),
            state_province=fake.country_code(),
            country=fake.current_country(),
            zip_code=fake.postcode(),
            time_zone="America/New_York",
            owner_name=fake.first_name_nonbinary(),
            owner_last_name=fake.last_name_nonbinary(),
            email=fake.ascii_email(),
            phone_number=fake.phone_number(),
            tax_id=fake.isbn13(),
        )
        await CompanyRepository.create(new_company, db)
        self.companies.append(new_company)

    async def bulk_creator(self, quantity: int, db: Session) -> List[Company]:
        """Creates n new companies and returns the list of new companies"""
        for _ in range(quantity):
            await self._company_creator(db)
        return self.companies
