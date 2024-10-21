import uuid
from typing import Annotated, Dict

from app.config import settings
from app.schemas.user import User
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from .generic_auth_provider import AuthProvider
from .mock_auth_provider import MockAuthProvider

security_scheme = HTTPBearer()


def get_auth_provider() -> AuthProvider:
    return MockAuthProvider()


async def get_access_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
) -> Dict[str, any] | HTTPException:
    try:
        payload = jwt.decode(
            token.credentials, "", algorithms=["HS256"], options={"verify_signature": False}
        )
        sub: str | None = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Could not validate credentials"
            )
        uuid.UUID(sub)
        access_token = auth_provider.authenticate_user(token.credentials)
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        ) from e
    except (JWTError, ValueError, AssertionError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token format"
        ) from e
    return access_token


async def get_current_user(
    access_token: Annotated[Dict[str, any], Depends(get_access_token)],
    auth_provider: Annotated[AuthProvider, Depends(get_auth_provider)],
    impersonation_sub: str | None = Query(None, description="Impersonation user sub."),
) -> User | HTTPException:
    user_data = auth_provider.get_user(access_token["sub"])
    user = User(
        id=uuid.UUID(user_data["id"], version=4),
        sub=user_data["sub"],
        username=user_data["username"],
        is_premium=user_data.get("is_premium", False),
        email=user_data.get("email", ""),
        groups=user_data.get("groups", []),
    )
    if not settings.auth_provider_enabled:
        return user
    try:
        # Additional logic here if needed
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
