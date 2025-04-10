from enum import Enum


class ColumnsLog(Enum):
  ALL = ['id', 'host', 'service', 'pid', 'message', 'datetime', 'time_execution', 'user_id']
  ORDER = ['host', 'service', 'pid', 'message', 'datetime', 'time_execution', 'target']
  FILTER_LIKE = ['host', 'service', 'pid', 'message', 'datetime', 'time_execution']
  ORDER_BY = ['ASC', 'DESC']
  ORDER_DESC = 'DESC'
  DATETIME = 'datetime'
