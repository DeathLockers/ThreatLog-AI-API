from ..enums.columns_log import ColumnsLog as EnumColumnsLog


def validate_order(order: str) -> str:

  if order not in EnumColumnsLog.ORDER.value:
    raise ValueError("Invalid order column")

  return order
