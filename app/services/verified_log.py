from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import VerifiedLog as ModelVerifiedLog
from ..schemas import UpsertVerifiedLog as SchemaUpsertVerifiedLog


def upsert_verified_log(db: Session, verified_log: SchemaUpsertVerifiedLog) -> bool:

  existing_verified_log = db.query(ModelVerifiedLog
                                   ).filter(ModelVerifiedLog.log_id == verified_log.log_id
                                            ).first()

  if existing_verified_log and verified_log.target == None:
    db.delete(existing_verified_log)
    db.commit()
    return True
  
  if verified_log.target == None:
    return True

  if not existing_verified_log:
    db_verified_log = ModelVerifiedLog(
      **verified_log.model_dump(),
      id=uuid4()
    )

    db.add(db_verified_log)
  else:
    existing_verified_log.target = verified_log.target

  db.commit()

  return True
