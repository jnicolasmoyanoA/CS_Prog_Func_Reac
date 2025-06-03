# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.userRoute import router as user_router
from database.pool import get_pool, close_pool  # Si quieres manejar eventos del pool

app = FastAPI(
    title="Crypto API Demo",
    description="Registro de usuarios y consulta de velas",
    version="1.0.0"
)

# Configurar CORS para conectar con frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a tu frontend luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(user_router)

# Eventos opcionales (por si quieres iniciar/cerrar pool)
@app.on_event("startup")
async def startup_event():
    await get_pool()

@app.on_event("shutdown")
async def shutdown_event():
    await close_pool()
