# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.userRoute import router as user_router
from routes.serviceRoute import router as service_router
from routes.socketRoute import router as socket_router

app = FastAPI(
    title="Crypto API Demo",
    description="Registro de usuarios y consulta de velas",
    version="1.0.0"
)

# Configurar CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(user_router)
app.include_router(service_router)
app.include_router(socket_router)

# Rutas raíz y de salud
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de Crypto Demo"}
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}

