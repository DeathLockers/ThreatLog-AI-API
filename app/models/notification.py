from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from ..db import Base


class Notification(Base):
  __tablename__ = "notifications"

  id = Column(String(150), primary_key=True)
  is_read = Column(Boolean, default=False, nullable=False)
  datetime = Column(DateTime, nullable=False)
  log_id = Column(String(150), ForeignKey("logs.id"), unique=True)

  log = relationship("Log", back_populates="notification", uselist=False)
