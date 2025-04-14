from ..enums.columns_log import ColumnsLog as EnumColumnsLog


def validate_order_by(order_by: str) -> str:

  if order_by not in EnumColumnsLog.ORDER_BY.value:
    raise ValueError("Invalid order. The order must be either 'ASC' or 'DESC'.")

  return order_by
