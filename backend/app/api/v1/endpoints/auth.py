from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token, UserResponse, UserLogin
from app.core.security import create_access_token
from app.services.auth_service import AuthService
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, returns a JWT access token.
    Accepts email in username field.
    """
    user = AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user["email"],
        role=user["role"].value,
        name=user["name"],
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user["role"].value,
        name=user["name"],
        email=user["email"],
    )


@router.post("/login/json", response_model=Token, tags=["Authentication"])
async def login_json(credentials: UserLogin):
    """JSON-based login endpoint for frontend client convenience."""
    user = AuthService.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        subject=user["email"],
        role=user["role"].value,
        name=user["name"],
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user["role"].value,
        name=user["name"],
        email=user["email"],
    )


@router.get("/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """Retrieve the current logged-in user profile with role permissions."""
    return current_user
