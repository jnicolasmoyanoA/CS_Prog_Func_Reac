from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from dto.userDTO import UserCreate, UserOut
from models.user import User
from config.security import hash_password
from database.pool import get_pool

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Verificar si ya existe
        existing = await conn.fetchrow("SELECT * FROM users WHERE email=$1", user.email)
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        hashed = hash_password(user.password)
        result = await conn.fetchrow(
            """
            INSERT INTO users (nombre, apellido, edad, email, hashed_password)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, nombre, apellido, edad, email
            """,
            user.nombre, user.apellido, user.edad, user.email, hashed
        )
        return dict(result)

