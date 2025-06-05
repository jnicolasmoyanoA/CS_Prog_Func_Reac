from dto.userDTO import UserCreate, LoginRequest
from config.security import hash_password, verify_password, create_access_token
from database.pool import get_pool
from fastapi import HTTPException

async def register_user_service(user: UserCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
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

async def login_user_service(credentials: LoginRequest):
    pool = await get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE email=$1", credentials.email)
        if not user or not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token = create_access_token(data={"sub": user["email"]})
        return {"access_token": token}
