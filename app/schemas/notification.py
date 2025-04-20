from typing import Optional
from pydantic import BaseModel
from .log import LogNotification as SchemaLogNotification


class NotificationBase(BaseModel):
  id: str
  # datetime: Datetime
  # is_read: int
  # log_id: str


class Notification(NotificationBase):
  log: Optional[SchemaLogNotification] = None

  class Config:
    from_attributes = True
