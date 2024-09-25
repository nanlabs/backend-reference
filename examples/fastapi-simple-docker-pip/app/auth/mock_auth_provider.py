from typing import Any, List, Dict
from .generic_auth_provider import AuthProvider

class MockAuthProvider(AuthProvider):
    def authenticate_user(self, token: str) -> Dict[str, Any]:
        return {
            "sub": "123e4567-e89b-12d3-a456-426614174000",
            "username": "mockuser",
            "is_premium": True,
            "email": "mockuser@example.com",
            "groups": ["user", "admin"]
        }

    def get_user(self, user_id: str) -> Dict[str, Any]:
        return {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "sub": "123e4567-e89b-12d3-a456-426614174000",
            "username": "mockuser",
            "is_premium": True,
            "email": "mockuser@example.com",
            "groups": ["user", "admin"]
        }

    def create_user(self, email: str, attributes: List[Dict[str, Any]], groups: List[str]) -> Dict[str, Any]:
        return {
            "response": "User created successfully"
        }

    def update_user(self, email: str, attributes: List[Dict[str, Any]], groups: List[str]) -> None:
        pass

    def delete_user(self, email: str) -> None:
        pass

    def set_user_password(self, email: str, password: str, permanent: bool = True) -> None:
        pass
