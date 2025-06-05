import asyncpg
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "min_size": 1,
    "max_size": 5
}

pool = None

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(**DB_CONFIG)
        print("✅ Pool de conexiones creado.")
    return pool

async def close_pool():
    global pool
    if pool:
        await pool.close()
        pool = None
        print("🔒 Pool de conexiones cerrado.")

async def fetch_all(query: str, params: dict = None):
    conn = await get_pool()
    async with conn.acquire() as connection:
        statement = await connection.prepare(query)
        if params:
            result = await statement.fetch(*params.values())
        else:
            result = await statement.fetch()
        return result
