from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import (PredictedLog as ModelPredictedLog)


def insert_predicted_log(db: Session, log_id: str, target: bool) -> str:

  id = str(uuid4())

  db_predicted_log = ModelPredictedLog(
    id=id,
    host=0,
    service=0,
    pid=0,
    message=0,
    timestamp=0,
    time_execution=0,
    target=target,
    log_id=log_id
  )

  db.add(db_predicted_log)

  return id
