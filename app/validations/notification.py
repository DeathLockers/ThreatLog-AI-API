from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_notification


def notification_id_exists(user_id: str, notification_id: str):
  with Session(engine) as db:
    if not get_notification(db, user_id, notification_id):
      raise ValueError("notification_id_not_exists")
    return True
