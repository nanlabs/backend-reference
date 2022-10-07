from fastapi import APIRouter, status

from models.user_model import Users, UsersList
from services.user_service import UsersService

router = APIRouter()
user_service = UsersService()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UsersList,
    name="Get All Users",
)
async def all_users():
    return user_service.get_all_user()


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=Users,
    name="Get User by Id",
)
async def get_user_by_id(user_id: int) -> Users:
    return user_service.get_user(user_id)


@router.put(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=Users,
    name="Update User by Id",
)
async def put_user(user_id: int) -> Users:
    return user_service.get_user(user_id)


@router.put(
    "/{user_id}/exc",
    status_code=status.HTTP_200_OK,
    response_model=Users,
    name="Update User by Id",
    deprecated=True
)
async def dep_get_user_by_id(user_id: int) -> Users:
    return user_service.get_user(user_id)
