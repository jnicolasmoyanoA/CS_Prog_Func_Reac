import sys
import os
import time
import asyncio
import websockets
import json
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ROOT_DIR)

from backend.data.extraction_data_crypto import connect_db, close_db, insert_active_candle, insert_closed_candle

# Tokens a escuchar
TOKENS = ["btcusdt", "ethusdt", "bnbusdt", "xrpusdt", "solusdt", "adausdt"]
STREAMS = '/'.join([f"{token}@kline_5m" for token in TOKENS])
URL = f"wss://fstream.binance.com/stream?streams={STREAMS}"

def parse_kline(msg: str) -> dict:
    data = json.loads(msg)
    k = data["data"]["k"]
    return {
        "symbol": data["data"]["s"].lower(),
        "interval": k["i"],
        "open_time": datetime.fromtimestamp(k["t"] / 1000),
        "close_time": datetime.fromtimestamp(k["T"] / 1000),
        "open": float(k["o"]),
        "high": float(k["h"]),
        "low": float(k["l"]),
        "close": float(k["c"]),
        "volume": float(k["v"]),
        "is_closed": k["x"],
        "updated_at": int(time.time() * 1000)
    }

async def listen_to_klines():
    await connect_db()
    try:
        async with websockets.connect(URL) as ws:
            print("📡 Escuchando velas de 5m de:", ", ".join([t.upper() for t in TOKENS]))
            while True:
                msg = await ws.recv()
                candle = parse_kline(msg)
                token = candle["symbol"]
                await insert_active_candle(token, candle)
                if candle["is_closed"]:
                    await insert_closed_candle(token, candle)
                print(f"[{candle['updated_at']}] {token.upper()} close = {candle['close']} volumen = {candle['volume']}")
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(listen_to_klines())
