from fastapi import APIRouter
from dto.userDTO import UserCreate, UserOut, LoginRequest, TokenResponse
from services.userService import register_user_service, login_user_service

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    return await register_user_service(user)

@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: LoginRequest):
    return await login_user_service(credentials)
