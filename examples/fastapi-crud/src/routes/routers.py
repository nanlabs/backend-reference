from fastapi import APIRouter

from controllers import company_controllers, employee_controllers

api_router = APIRouter(prefix="/api/v0")

api_router.include_router(company_controllers.router, tags=["Companies"], prefix="/companies")
api_router.include_router(employee_controllers.router, tags=["Employees"], prefix="/employees")
