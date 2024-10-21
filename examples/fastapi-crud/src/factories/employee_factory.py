import random
from typing import List
from uuid import uuid4

from faker import Faker
from models.models import Company, Employee
from repositories.employee_repository import EmployeeRepository
from sqlalchemy.orm import Session

faker = Faker()


class EmployeesFactory:
    """Generates Employees in the DB"""

    def __init__(self) -> None:
        self.employees = list()

    async def _employee_creator(self, db: Session, company_id) -> None:
        """Creates new employee in db with fake info"""
        fake = Faker()
        new_employee = Employee(
            id=str(uuid4()),
            first_name=fake.first_name_nonbinary(),
            last_name=fake.last_name_nonbinary(),
            address=fake.street_address(),
            city=fake.city(),
            state_province=fake.country_code(),
            country=fake.current_country(),
            zip_code=fake.postcode(),
            time_zone="America/New_York",
            personal_id=fake.ssn(),
            email=fake.ascii_email(),
            phone_number=fake.phone_number(),
            is_manager=fake.pybool(),
            avatar_url="https://i.pravatar.cc/300",
            company=company_id,
            role=fake.job(),
        )
        await EmployeeRepository.create(new_employee, db)
        self.employees.append(new_employee)

    async def bulk_creator_for_company(
        self, quantity: int, db: Session, company_id: str | None = None
    ):
        """Creates n new employees for a given company_id"""
        for _ in range(quantity):
            await self._employee_creator(db, company_id)
        return self.employees

    async def bulk_creator(self, quantity: int, db: Session, companies: List[Company]):
        for _ in range(quantity):
            await self._employee_creator(db=db, company_id=random.choice(companies).id)
        return self.employees
