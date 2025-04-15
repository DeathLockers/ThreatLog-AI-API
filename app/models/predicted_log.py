from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base


class PredictedLog(Base):
  __tablename__ = "predicted_logs"

  id = Column(String(150), primary_key=True)
  host = Column(Integer, CheckConstraint('host <= 999999999'), nullable=False) # 9 digits
  service = Column(Integer, CheckConstraint('service <= 999999999'), nullable=False) # 9 digits
  pid = Column(Integer, CheckConstraint('pid <= 999999'), nullable=False) # 6 digits
  message = Column(Integer, CheckConstraint('message <= 999999999'), nullable=False) # 9 digits
  timestamp = Column(Integer, nullable=False)
  time_execution = Column(Integer, CheckConstraint('time_execution <= 999999999'), nullable=False) # 9 digits
  target = Column(Boolean, nullable=False)
  log_id = Column(String(150), ForeignKey("logs.id"), unique=True)
  
  log = relationship("Log", back_populates="predicted_log", uselist=False)
