import unittest

from models.schemas.company import NewCompanySchema, PatchCompanySchema
from models.schemas.employee import NewEmployeeSchema, PatchEmployeeSchema


class OptionalSchemaFieldsTest(unittest.TestCase):
    def test_company_create_keeps_nullable_fields_optional(self) -> None:
        company = NewCompanySchema(
            company_name="Example",
            address="1 Main St",
            city="Example City",
            state_province="CA",
            country="US",
            email="owner@example.com",
            tax_id="123",
        )

        self.assertIsNone(company.address_line_2)
        self.assertIsNone(company.phone_number)

    def test_employee_create_keeps_nullable_fields_optional(self) -> None:
        employee = NewEmployeeSchema(
            first_name="Ada",
            last_name="Lovelace",
            address="1 Main St",
            city="Example City",
            state_province="CA",
            country="US",
            personal_id="123",
            email="ada@example.com",
            phone_number="555-0100",
            role="Engineer",
        )

        self.assertIsNone(employee.zip_code)
        self.assertIsNone(employee.company)
        self.assertIsNone(employee.avatar_url)

    def test_patch_schemas_accept_sparse_payloads(self) -> None:
        company_patch = PatchCompanySchema.model_validate({"city": "New City"})
        employee_patch = PatchEmployeeSchema.model_validate({"role": "Engineer"})

        self.assertEqual(
            company_patch.model_dump(exclude_unset=True), {"city": "New City"}
        )
        self.assertEqual(
            employee_patch.model_dump(exclude_unset=True), {"role": "Engineer"}
        )
