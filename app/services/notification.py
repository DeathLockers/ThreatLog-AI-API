from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4
import pytz
from sqlalchemy import (desc)
from sqlalchemy.orm import Session
from ..models import (Notification as ModelNotification,
                      Log as ModelLog)
from ..core import getenv


def get_notification(db: Session, user_id: str, notification_id: str):
  return db.query(ModelNotification
                  ).join(ModelLog, ModelNotification.log_id == ModelLog.id
                         ).filter(ModelNotification.id == notification_id, ModelLog.user_id == user_id
                                  ).first()


def get_all_notifications(db: Session, user_id: str):
  return db.query(ModelNotification
                  ).join(ModelLog, ModelNotification.log_id == ModelLog.id
                         ).filter(ModelNotification.is_read == False, ModelLog.user_id == user_id
                                  ).order_by(desc(ModelNotification.datetime)).all()


def insert_notification(db: Session, log_id: str) -> str:

  id = str(uuid4())

  db_notification = ModelNotification(
      log_id=log_id,
      datetime=datetime.now(pytz.timezone(getenv("TIMEZONE"))),
      id=id
    )

  db.add(db_notification)

  return id


def update_read_notification(db: Session, user_id: str, notification_id: str):
  notification = db.query(ModelNotification
                          ).join(ModelLog, ModelNotification.log_id == ModelLog.id
                                 ).filter(ModelNotification.id == notification_id, ModelLog.user_id == user_id
                                          ).first()

  notification.is_read = True

  db.commit()

  return True


def update_all_read_notifications(db: Session, user_id: str):
  notifications = db.query(ModelNotification
                           ).join(ModelLog, ModelNotification.log_id == ModelLog.id
                                  ).filter(ModelLog.user_id == user_id, ModelNotification.is_read == False
                                           ).all()

  for notification in notifications:
    notification.is_read = True

  db.commit()

  return True
