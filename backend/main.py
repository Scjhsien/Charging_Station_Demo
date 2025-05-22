from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from typing import List, Dict
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# WebSocket connection pools
class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {
            'homepage': [],
            'simulator': []
        }

    async def connect(self, websocket: WebSocket, client_type: str):
        await websocket.accept()
        self.connections[client_type].append(websocket)

    def disconnect(self, websocket: WebSocket):
        for client_type in self.connections:
            if websocket in self.connections[client_type]:
                self.connections[client_type].remove(websocket)

    async def broadcast_to(self, client_type: str, message: str):
        for connection in self.connections[client_type]:
            await connection.send_text(message)

    async def broadcast_all(self, message: str):
        for client_type in self.connections:
            await self.broadcast_to(client_type, message)

manager = ConnectionManager()

@app.websocket("/ws/station")
async def station_websocket(websocket: WebSocket):
    await manager.connect(websocket, 'simulator')
    try:
        while True:
            data = await websocket.receive_text()
            print("Simulator 傳送", data)
            await manager.broadcast_to('homepage', data)
    except WebSocketDisconnect:
        print("Simulator 離線")
        manager.disconnect(websocket)

@app.websocket("/ws/homepage")
async def homepage_websocket(websocket: WebSocket):
    await manager.connect(websocket, 'homepage')
    try:
        while True:
            data = await websocket.receive_text()
            print("Homepage 傳送", data)
            await manager.broadcast_to('simulator', data)
    except WebSocketDisconnect:
        print("Homepage 離線")
        manager.disconnect(websocket)
