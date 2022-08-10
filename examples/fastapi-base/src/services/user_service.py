import logging

from factories.user_factory import UserFactory
from models.user_model import Users, UsersList

logger = logging.getLogger(__name__)


class UsersService:

    def get_all_user(self) -> UsersList:
        return [UserFactory() for i in range(10)]

    def get_user(self, user_id: int) -> Users:
        return UserFactory(id=user_id)
