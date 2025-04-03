from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
  def __init__(self):
    self.active_connections: Dict[str, WebSocket] = {}

  async def connect(self, websocket: WebSocket, user_id: str):
    await websocket.accept()
    self.active_connections[user_id] = websocket

  def disconnect(self, user_id: str):
    if user_id in self.active_connections:
      del self.active_connections[user_id]

  async def send_personal_message(self, message: dict, user_id: str):
    websocket = self.active_connections.get(user_id)
    if websocket:
      await websocket.send_json(message)

  async def broadcast(self, message: str):
    for connection in self.active_connections.values():
      await connection.send_text(message)


connection_manager = ConnectionManager()
