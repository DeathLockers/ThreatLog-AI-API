from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import (PredictedLog as ModelPredictedLog)
from ..schemas import (PredictedLogKafkaConsumser as SchemaPredictedLogKafkaConsumser)


def insert_predicted_log(db: Session, predicted_log: SchemaPredictedLogKafkaConsumser) -> bool:

  db_predicted_log = ModelPredictedLog(
      **predicted_log.model_dump(),
      id=uuid4()
    )

  db.add(db_predicted_log)
  db.commit()

  return True
