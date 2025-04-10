from sqlalchemy.orm import Session
from ..db import engine
from ..services import get_log


def log_id_exists(log_id: str):
  with Session(engine) as db:
    if not get_log(db, log_id):
      raise ValueError("log_id_not_exists")
    return log_id
