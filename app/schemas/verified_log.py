from typing import Optional
from importlib import import_module
from pydantic import BaseModel
from pydantic import (BaseModel, field_validator)


class VerifiedLogBase(BaseModel):
  # id: str
  target: bool
  # log_id: str


class VerifiedLog(VerifiedLogBase):
  class Config:
    from_attributes = True


class UpsertVerifiedLog(BaseModel):
  log_id: str
  target: Optional[bool]

  @field_validator("log_id")
  @classmethod
  def car_fuel_id_exists(cls, log_id: str):
    validator = import_module("app.validations.log")
    return validator.log_id_exists(log_id)

  @field_validator("target")
  @classmethod
  def target_is_exists(cls, target: bool):
    if not isinstance(target, bool):
      return None
    else:
      return target
