import os
import sys
import asyncpg

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ROOT_DIR)

from backend.database.pool import get_pool

async def insert_active_candle(token: str, candle: dict):
    pool = await get_pool()

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
    pool = await get_pool()

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
