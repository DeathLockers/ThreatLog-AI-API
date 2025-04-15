from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from ..db import Base


class VerifiedLog(Base):
  __tablename__ = "verified_logs"

  id = Column(String(150), primary_key=True)
  target = Column(Boolean, nullable=False)
  log_id = Column(String(150), ForeignKey("logs.id"), unique=True)
  
  log = relationship("Log", back_populates="verified_log", uselist=False)
