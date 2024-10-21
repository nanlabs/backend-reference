from typing import List

from db.database import get_db
from fastapi import APIRouter, Depends, status
from models.schemas.company import CompanySchema, NewCompanySchema, PatchCompanySchema
from services.company_service import CompanyService
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/mock-company/{quantity}",
    status_code=status.HTTP_201_CREATED,
    name="Create and get n mock company",
    response_model=List[CompanySchema],
)
async def mock_company_creator(quantity: int, db: Session = Depends(get_db)):
    return await CompanyService.bulk_creator(quantity, db)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="Get all companies",
    response_model=List[CompanySchema],
)
async def get_all_companies(db: Session = Depends(get_db)):
    return await CompanyService.get_all(db)


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, name="Get Company by Id", response_model=CompanySchema
)
async def get_company(id: str, db: Session = Depends(get_db)):
    return await CompanyService.get_by_id(id, db)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    name="Modify company by Id",
    response_model=CompanySchema,
)
async def update_company(id: str, request: PatchCompanySchema, db: Session = Depends(get_db)):
    return await CompanyService.patch(id, request, db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="Create new company",
    response_model=CompanySchema,
)
async def new_company(request: NewCompanySchema, db: Session = Depends(get_db)):
    return await CompanyService.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, name="Delete company by id")
async def delete_company(id: str, db: Session = Depends(get_db)):
    return await CompanyService.delete_company(id, db)
