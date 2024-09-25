from abc import ABC, abstractmethod
from typing import Any, List, Dict

class AuthProvider(ABC):
    @abstractmethod
    def authenticate_user(self, token: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_user(self, email: str, attributes: List[Dict[str, Any]], groups: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_user(self, email: str, attributes: List[Dict[str, Any]], groups: List[str]) -> None:
        pass

    @abstractmethod
    def delete_user(self, email: str) -> None:
        pass

    @abstractmethod
    def set_user_password(self, email: str, password: str, permanent: bool = True) -> None:
        pass
