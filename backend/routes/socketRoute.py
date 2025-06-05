from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from backend.binance.data_stream import listen_to_klines
from backend.dto.activeCandleDTO import ActiveCandleStreamDTO

router = APIRouter()
clients: list[WebSocket] = []

@router.websocket("/ws/candles")
async def websocket_candles(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    async def send_to_clients(candle_dict):
        dto = ActiveCandleStreamDTO(**candle_dict)
        message = dto.json()

        disconnected = []

        for client in clients:
            try:
                await client.send_text(message)
            except Exception as e:
                print(f"❌ Error enviando a cliente: {e}")
                disconnected.append(client)
                for client in disconnected:
                    clients.remove(client)

    try:
        await listen_to_klines(callback=send_to_clients)
    except WebSocketDisconnect:
        clients.remove(websocket)
        await websocket.close()
        print("🔌 Cliente desconectado")
