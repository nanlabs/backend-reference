from typing import List

from db.database import get_db
from fastapi import APIRouter, Depends, status
from models.schemas.company import NewCompanySchema
from models.schemas.employee import EmployeeSchema, PatchEmployeeSchema, ShortEmployeeSchema
from services.employee_service import EmployeeService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/mock-employee/{quantity}",
    status_code=status.HTTP_200_OK,
    name="Generate mock employees",
    response_model=List[EmployeeSchema],
)
async def mock_employee_creator(
    quantity: int, db: Session = Depends(get_db), company_id: str = None
):
    return await EmployeeService.bulk_creator(quantity, db, company_id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="Get all employees",
    response_model=List[ShortEmployeeSchema],
)
async def get_all_employees(db: Session = Depends(get_db), company_id: str = None):
    if company_id is not None:
        return await EmployeeService.get_all_for_company(company_id, db)
    return await EmployeeService.get_all(db)


@router.get(
    "/{id}/",
    status_code=status.HTTP_200_OK,
    name="Get employee by Id",
)
async def get_employee(id: str, db: Session = Depends(get_db)):
    return await EmployeeService.get_by_id(id, db)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    name="Modify employee by Id",
    response_model=EmployeeSchema,
)
async def update_company(id: str, request: PatchEmployeeSchema, db: Session = Depends(get_db)):
    return await EmployeeService.patch(id, request, db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="Create a employee",
    response_model=EmployeeSchema,
)
async def new_employee(request: NewCompanySchema, db: Session = Depends(get_db)):
    return await EmployeeService.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete employee by id")
async def delete_company(id: str, db: Session = Depends(get_db)):
    return await EmployeeService.delete_employee(id, db)
