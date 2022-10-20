from db.database import Base
from sqlalchemy import Column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String


class Company(Base):
    __tablename__ = 'company'
    id = Column(String, primary_key=True, index=True, unique=True)
    company_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address_line_2 = Column(String)
    city = Column(String, nullable=False)
    state_province = Column(String, nullable=False)
    country = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    time_zone = Column(String)
    owner_name = Column(String)
    owner_last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    tax_id = Column(String, nullable=False)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(String, primary_key=True, index=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state_province = Column(String, nullable=False)
    country = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    time_zone = Column(String)
    personal_id = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    is_manager = Column(Boolean)
    avatar_url = Column(String)
    company = Column(String, ForeignKey('company.id'))
    role = Column(String)
