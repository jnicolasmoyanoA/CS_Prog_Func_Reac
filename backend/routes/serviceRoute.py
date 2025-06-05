import sys
import os
from fastapi import APIRouter, Query
from typing import List

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ROOT_DIR)

from backend.dto.activeCandleDTO import ActiveCandleStreamDTO
from backend.services.candleService import get_recent_active_candles

router = APIRouter(prefix="/candles", tags=["Candles"])

@router.get("/active/stream", response_model=List[ActiveCandleStreamDTO])
async def get_active_candle_stream(limit: int = Query(5000, ge=1, le=5000)):
    """
    Devuelve las últimas 'limit' velas activas.
    """
    return await get_recent_active_candles(limit)

