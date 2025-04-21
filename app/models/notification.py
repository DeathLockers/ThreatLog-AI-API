from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from ..db import Base
from ..core import getenv


class Notification(Base):
  __tablename__ = "notifications"

  id = Column(String(150), primary_key=True)
  is_read = Column(Boolean, nullable=False)
  datetime = Column(DateTime, default=datetime.now(ZoneInfo(getenv("TIMEZONE"))), nullable=False)
  log_id = Column(String(150), ForeignKey("logs.id"), unique=True)

  log = relationship("Log", back_populates="notification", uselist=False)
