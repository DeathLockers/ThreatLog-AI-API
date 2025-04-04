from pydantic import BaseModel


class PredictedLogBase(BaseModel):
  # id: str
  # host: int
  # service: int
  # pid: int
  # message: int
  # timestamp: int
  # time_execution: int
  target: bool
  # log_id: str


class PredictedLog(PredictedLogBase):
  class Config:
    from_attributes = True
