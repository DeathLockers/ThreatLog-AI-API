from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base


class Log(Base):
  __tablename__ = "logs"

  id = Column(String(150), primary_key=True)
  host = Column(String(150), nullable=False)
  service = Column(String(150), nullable=False)
  pid = Column(Integer, CheckConstraint('pid <= 999999'), nullable=False) # 6 digits
  message = Column(String(255), nullable=True)
  datetime = Column(DateTime, nullable=False)
  time_execution = Column(Integer, CheckConstraint('time_execution <= 999999999'), nullable=False) # 9 digits
  user_id = Column(String(150), ForeignKey("users.id"))
	
  user = relationship("User", back_populates="logs", lazy="subquery")
  predicted_log = relationship("PredictedLog", back_populates="log", uselist=False)
  verified_log = relationship("VerifiedLog", back_populates="log", uselist=False)