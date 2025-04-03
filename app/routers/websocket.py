from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..core import connection_manager, get_current_user_wewbsocket


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  token = websocket.headers.get("Authorization")

  user = get_current_user_wewbsocket(token)

  await connection_manager.connect(websocket, user.id)

  try:
    while True:
      data = await websocket.receive_text()
      await connection_manager.send_personal_message(data, user.id)
  except WebSocketDisconnect:
    connection_manager.disconnect(user.id)
