from typing import Optional, Dict
from app.schemas.auth import RoleEnum, UserResponse
from app.core.security import get_password_hash, verify_password

# Demo user credentials with hashed passwords
# Inspector: inspector@shram.gov.in / Inspector@123
# Employer: employer@abcindustries.com / Employer@123
# Admin: admin@shram.gov.in / Admin@123

DEMO_USERS: Dict[str, dict] = {
    "inspector@shram.gov.in": {
        "id": "USR-INSP-01",
        "email": "inspector@shram.gov.in",
        "hashed_password": get_password_hash("Inspector@123"),
        "name": "S. K. Sharma",
        "role": RoleEnum.INSPECTOR,
        "designation": "Assistant Labour Commissioner (Central)",
        "jurisdiction": "Delhi & NCR Region",
        "establishment_id": None,
    },
    "employer@abcindustries.com": {
        "id": "USR-EMP-01",
        "email": "employer@abcindustries.com",
        "hashed_password": get_password_hash("Employer@123"),
        "name": "Rajiv Mehra",
        "role": RoleEnum.EMPLOYER,
        "designation": "Compliance Officer & Factory Manager",
        "jurisdiction": None,
        "establishment_id": "EST-001",
    },
    "admin@shram.gov.in": {
        "id": "USR-ADM-01",
        "email": "admin@shram.gov.in",
        "hashed_password": get_password_hash("Admin@123"),
        "name": "Dr. V. Ramanathan",
        "role": RoleEnum.ADMIN,
        "designation": "Chief Labour Intelligence Administrator",
        "jurisdiction": "National Enforcement Sphere",
        "establishment_id": None,
    },
}


class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[dict]:
        user = DEMO_USERS.get(email.lower())
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserResponse]:
        user = DEMO_USERS.get(email.lower())
        if not user:
            return None
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user["role"],
            designation=user["designation"],
            jurisdiction=user["jurisdiction"],
            establishment_id=user["establishment_id"],
        )
