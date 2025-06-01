import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "min_size": 1,
    "max_size": 5
}

pool = None

async def connect_db():
    global pool
    pool = await asyncpg.create_pool(**DB_CONFIG)
    print("✅ Conexión a PostgreSQL lista.")

async def close_db():
    global pool
    if pool:
        await pool.close()
        print("🔒 Conexión a PostgreSQL cerrada.")

async def insert_active_candle(token: str, candle: dict):
    insert_query = """
        INSERT INTO active_candles (
            token, open_time, close_time, open, high, low, close, volume, is_closed, updated_at
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
    """
    delete_query = """
        DELETE FROM active_candles
        WHERE token = $1 AND open_time NOT IN (
            SELECT open_time FROM active_candles
            WHERE token = $1
            ORDER BY open_time DESC
            LIMIT 50
        );
    """
    async with pool.acquire() as conn:
        await conn.execute(insert_query,
            token,
            candle["open_time"],
            candle["close_time"],
            candle["open"],
            candle["high"],
            candle["low"],
            candle["close"],
            candle["volume"],
            candle["is_closed"],
            candle["updated_at"]
        )
        await conn.execute(delete_query, token)


async def insert_closed_candle(token: str, candle: dict):
    query = """
        INSERT INTO closed_candles (
            token, open_time, close_time, open, high, low, close, volume
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        ON CONFLICT (token, open_time)
        DO NOTHING;
    """
    async with pool.acquire() as conn:
        await conn.execute(query,
            token,
            candle["open_time"],
            candle["close_time"],
            candle["open"],
            candle["high"],
            candle["low"],
            candle["close"],
            candle["volume"]
        )
