from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    edad: int = Field(..., ge=1, le=120)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    edad: int
    email: EmailStr

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"