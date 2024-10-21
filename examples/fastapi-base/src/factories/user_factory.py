import factory
from faker import Factory
from models.user_model import Users

faker = Factory.create()


class UserFactory(factory.Factory):
    class Meta:
        model = Users

    id = factory.LazyAttribute(lambda x: faker.random_int(min=1))
    name = factory.LazyAttribute(lambda x: faker.name())
    address = factory.LazyAttribute(lambda x: faker.street_address())
    city = factory.LazyAttribute(lambda x: faker.city())
    country = factory.LazyAttribute(lambda x: faker.country())
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    age = factory.LazyAttribute(lambda x: faker.random_int(min=1, max=75))
    license = factory.LazyAttribute(lambda x: faker.license_plate())


if __name__ == "__main__":
    print(UserFactory())
