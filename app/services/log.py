from datetime import datetime, timedelta
import uuid
import pytz
from sqlalchemy.orm import Session
from sqlalchemy import (cast,
                        desc,
                        func,
                        String,
                        Integer,
                        Float,
                        DateTime,
                        and_,
                        or_)
from ..models import (Log as ModelLog,
                      PredictedLog as ModelPredictedLog)
from ..schemas import (LogFilter as SchemaLogFilter,
                       User as SchemaUser)
from ..core import getenv
from ..enums.predicted_log_targets import PredictedLogTargets
from ..enums.columns_log import ColumnsLog


def get_log(db: Session, log_id: str):
  return db.query(ModelLog
                  ).filter(ModelLog.id == log_id).first()


def get_logs(db: Session, user: SchemaUser, filters: SchemaLogFilter):

  skip = (filters.page - 1) * filters.items

  query = db.query(ModelLog)

  # Filter range dates
  if not filters.range_date:
    end_date = datetime.now(pytz.timezone(getenv("TIMEZONE")))
    start_date = end_date - timedelta(weeks=1)

    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
  else:
    start_date = filters.range_date[0]
    end_date = filters.range_date[1]

  query = query.filter(ModelLog.datetime >= start_date, ModelLog.datetime <= end_date)

  # Filter target
  if filters.target:
    query = query.join(ModelPredictedLog, ModelLog.id == ModelPredictedLog.log_id)
    query = query.filter(ModelPredictedLog.target == filters.target)

  # Filter user
  query = query.filter(ModelLog.user_id == user.id)

  # Filter LIKE
  if filters.filter:
    query = filter_search_words(query, filters.filter)

  # Order by
  column = getattr(ModelLog, filters.order, None)

  if filters.order_by == 'DESC':
    query = query.order_by(desc(column))
  else:
    query = query.order_by(column)

  # Pagination
  query = query.offset(skip).limit(filters.items)

  return query.all()


def count_logs_in_time_periods(db: Session, user: SchemaUser, time_periods: list[str], minutes=5):
  logs_count = {}

  query = db.query(ModelLog)

  query = query.join(ModelPredictedLog, ModelLog.id == ModelPredictedLog.log_id
                     ).filter(ModelLog.user_id == user.id,
                              ModelPredictedLog.target == PredictedLogTargets.IS_ANOMALY.value)

  current_date = datetime.now().date()

  # Count by periods
  for time_slot in time_periods:
    start_time = datetime.strptime(f'{current_date} {time_slot}', '%Y-%m-%d %H:%M')
    end_time = start_time + timedelta(minutes=minutes)

    count = query.filter(ModelLog.datetime >= start_time, ModelLog.datetime < end_time
                         ).count()

    logs_count[time_slot] = count

  return logs_count


def total_type_logs_in_period(db: Session, user: SchemaUser):
  end_date = datetime.now(pytz.timezone(getenv("TIMEZONE")))
  start_date = end_date - timedelta(days=6)
  start_date = datetime.combine(start_date, datetime.min.time())

  anomaly_count = count_type_log(db,
                                 PredictedLogTargets.IS_ANOMALY.value,
                                 user.id,
                                 start_date,
                                 end_date)

  non_anomaly_count = count_type_log(db,
                                     PredictedLogTargets.NORMAL.value,
                                     user.id,
                                     start_date,
                                     end_date)

  return {
      "total_anomaly": anomaly_count,
      "total_non_anomaly": non_anomaly_count
  }


def count_type_logs_in_period(db: Session, user: SchemaUser):
  end_date = datetime.now(pytz.timezone(getenv("TIMEZONE")))
  start_date = end_date - timedelta(days=6)

  dates = [start_date + timedelta(days=i) for i in range(7)]

  daily_anomalies = {}
  daily_non_anomalies = {}

  for day in dates:
    day_start = datetime.combine(day, datetime.min.time())
    day_end = day_start + timedelta(days=1)

    anomaly_count = count_type_log(db,
                                   PredictedLogTargets.IS_ANOMALY.value,
                                   user.id,
                                   day_start,
                                   day_end)

    non_anomaly_count = count_type_log(db,
                                       PredictedLogTargets.NORMAL.value,
                                       user.id,
                                       day_start,
                                       day_end)

    daily_anomalies[day.strftime('%Y-%m-%d')] = anomaly_count
    daily_non_anomalies[day.strftime('%Y-%m-%d')] = non_anomaly_count

  return {
      "daily_anomalies": daily_anomalies,
      "daily_non_anomalies": daily_non_anomalies
    }


def count_type_log(db: Session, type_log: int, user_id: str, day_start: datetime, day_end: datetime):
  return db.query(func.count(ModelPredictedLog.id)).join(
      ModelLog, ModelLog.id == ModelPredictedLog.log_id
    ).filter(
        ModelPredictedLog.target == type_log,
        ModelLog.user_id == user_id,
        ModelLog.datetime >= day_start,
        ModelLog.datetime < day_end
    ).scalar()


def filter_search_words(query, search_words: str):
  words = search_words.split()
  word_filters = []

  for word in words:
    column_filters = []

    for column_name in ColumnsLog.FILTER_LIKE.value:
      column = getattr(ModelLog, column_name)

      if isinstance(column.type, String):
        column_filters.append(column.like(f"%{word}%"))
      elif isinstance(column.type, (Integer, Float, DateTime)):
        column_filters.append(cast(column, String).like(f"%{word}%"))

    if column_filters:
      word_filters.append(or_(*column_filters))

  if word_filters:
    query = query.filter(and_(*word_filters))

  return query

def inser_log(db: Session, user_id:str, message: str) -> str:
  model_log = ModelLog()
  model_log.id = str(uuid.uuid4())
  model_log.user_id = user_id
  model_log.message = message
  # TODO: fill host, service, pid
  model_log.host = 'mock'
  model_log.service = 'mock'
  model_log.pid = 1
  # TODO: not sure if this is correct
  model_log.datetime = datetime.now(pytz.timezone(getenv("TIMEZONE"))).astimezone(pytz.utc)
  # TODO: get time execution
  model_log.time_execution = 0
  db.add(model_log)
  return model_log.id

def insert_predicted(db: Session, log_id: str, message: str) -> str:
  model_log = ModelPredictedLog()
  model_log.id = str(uuid.uuid4())
  model_log.log_id = log_id
  # TODO: fill host, service, pid
  model_log.host = -1
  model_log.service = 'mock'
  model_log.message = message
  model_log.pid = 1
  # TODO: get time execution
  model_log.time_execution = 0
  # TODO: not sure if this is correct
  model_log.timestamp = datetime.now(pytz.timezone(getenv("TIMEZONE"))).astimezone(pytz.utc)
  db.add(model_log)
  return model_log.id

