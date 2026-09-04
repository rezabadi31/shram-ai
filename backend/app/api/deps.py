from typing import List, Callable, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.schemas.auth import UserResponse, RoleEnum
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> UserResponse:
    """Dependency: decodes JWT token and retrieves authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please authenticate.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    email: str = payload.get("sub")
    if not email:
        raise credentials_exception

    user = AuthService.get_user_by_email(email)
    if not user:
        raise credentials_exception

    return user


async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[UserResponse]:
    """Dependency: returns current user if valid token provided, else None."""
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    email: str = payload.get("sub")
    if not email:
        return None
    return AuthService.get_user_by_email(email)


def require_role(allowed_roles: List[str]) -> Callable:
    """Dependency factory: enforces Role-Based Access Control (RBAC)."""
    async def role_checker(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
        role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
        allowed_normalized = [r.lower() for r in allowed_roles]
        if role_val.lower() not in allowed_normalized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of the following roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return role_checker


async def require_employer(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Enforces that the authenticated user has the EMPLOYER role."""
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val.lower() != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Restricted — This portal is designated exclusively for registered Employers.",
        )
    return current_user


async def require_inspector(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Enforces that the authenticated user has the INSPECTOR or ADMIN role."""
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val.lower() not in ("inspector", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Restricted — Your account does not have Inspector permissions.",
        )
    return current_user


async def require_admin(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Enforces that the authenticated user has the ADMIN role."""
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Restricted — Administrative privileges required.",
        )
    return current_user


def verify_establishment_ownership(establishment_id: str, current_user: UserResponse) -> None:
    """
    Enforces that Employers can only access data for their own establishment.
    Does not trust establishment_id passed blindly from the client.
    """
    role_val = current_user.role.value if hasattr(current_user.role, 'value') else str(current_user.role)
    if role_val.lower() == "employer":
        if current_user.establishment_id and current_user.establishment_id != establishment_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Restricted — Employers may only access their own establishment records.",
            )


# Function aliases matching explicit specification:
requireEmployer = require_employer
requireInspector = require_inspector
requireAdmin = require_admin

