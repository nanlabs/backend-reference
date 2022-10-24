import factory
from faker import Factory

from models.company_model import Company_Pydantic

faker = Factory.create()


class CompanyFactory(factory.Factory):
    class Meta:
        model = Company_Pydantic

    id = factory.LazyAttribute(lambda x: faker.uuid4())
    company_name = factory.LazyAttribute(lambda x: faker.company())
    address = factory.LazyAttribute(lambda x: faker.street_address())
    city = factory.LazyAttribute(lambda x: faker.city())
    country = factory.LazyAttribute(lambda x: faker.country())
    zip_code = factory.LazyAttribute(lambda x: faker.postcode())
    time_zone = factory.LazyAttribute(lambda x: faker.timezone())
    owner_name = factory.LazyAttribute(lambda x: faker.first_name())
    owner_last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    tax_id = factory.LazyAttribute(lambda x: faker.ssn())
