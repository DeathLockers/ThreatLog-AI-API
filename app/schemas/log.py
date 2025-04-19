from importlib import import_module
from datetime import datetime
from typing import Optional
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import (BaseModel, computed_field, field_validator)
from .predicted_log import PredictedLog as SchemaPredictedLog
from .verified_log import VerifiedLog as SchemaVerifiedLog
from ..enums.columns_log import ColumnsLog as EnumColumnsLog


class LogBase(BaseModel):
  id: str
  host: str
  service: str
  pid: int
  message: str
  datetime: datetime
  time_execution: int
  # user_id: str


class LogFilter(BaseModel):
  items: int
  page: int
  filter: Optional[str] = ''
  range_date: Optional[list[str, str]] = None
  target: Optional[bool | str] = None
  order: Optional[str] = EnumColumnsLog.DATETIME.value
  order_by: Optional[str] = EnumColumnsLog.ORDER_DESC.value

  @field_validator("range_date")
  @classmethod
  def start_and_end_date_range(cls, range_date: list[str, str], info: FieldValidationInfo):
    validator = import_module("app.validations.validate_dates")
    return validator.validate_range_dates(range_date)

  @field_validator("target")
  @classmethod
  def target_is_exists(cls, target: bool):
    if not isinstance(target, bool):
      return None
    else:
      return target

  @field_validator("order")
  @classmethod
  def order_column_exists(cls, order: str):
    if not order:
      return EnumColumnsLog.DATETIME.value

    validator = import_module("app.validations.validate_order")
    return validator.validate_order(order)

  @field_validator("order_by")
  @classmethod
  def order_is_by_exists(cls, order_by: str):
    if not order_by:
      return EnumColumnsLog.ORDER_DESC.value

    validator = import_module("app.validations.validate_order_by")
    return validator.validate_order_by(order_by)


class Log(LogBase):
  predicted_log: Optional[SchemaPredictedLog] = None
  verified_log: Optional[SchemaVerifiedLog] = None

  class Config:
    from_attributes = True

  # @computed_field
  # @property
  # def predict_log(self) -> bool:
  #   return self.predicted_log.target


class LogChartLinePeriod(BaseModel):
  periods: list[str]
  total: list[int]


class LogTypesTotal(BaseModel):
  total_anomaly: int
  total_non_anomaly: int


class LogChartTypesCountPeriodList(BaseModel):
  dates: list[str]
  count: list[int]


class LogChartTypesCountPeriod(BaseModel):
  daily_anomalies: LogChartTypesCountPeriodList
  daily_non_anomalies: LogChartTypesCountPeriodList


class LogRawKafkaConsumer(BaseModel):
  log_host: str
  log_service: str
  log_pid: int
  log_message: str
  log_datetime: datetime
  log_time_execution: int
  log_user_id: str
  predicted_log_host: int
  predicted_log_service: int
  predicted_log_pid: int
  predicted_log_message: int
  predicted_log_timestamp: int
  predicted_log_time_execution: int
  predicted_log_target: bool


class LogKafkaConsumser(BaseModel):
  host: str
  service: str
  pid: int
  message: str
  datetime: str
  time_execution: int
  user_id: str
