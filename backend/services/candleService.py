import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ROOT_DIR)

from backend.database.pool import fetch_all
from backend.dto.activeCandleDTO import ActiveCandleStreamDTO

async def get_recent_active_candles(limit: int = 5000):
    query = """
        SELECT token, open_time, updated_at, open, high, low, close, volume
        FROM active_candles
        WHERE is_closed = FALSE
        ORDER BY updated_at DESC
        LIMIT $1
    """
    rows = await fetch_all(query, {"limit": limit})
    return [ActiveCandleStreamDTO(**dict(row)) for row in rows]

