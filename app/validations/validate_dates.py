from datetime import datetime


def validate_range_dates(range_dates: list[str, str]):
  if not range_dates:
    return None

  if len(range_dates) == 2:
    start = range_dates[0]
    end = range_dates[1]
  elif len(range_dates) == 1:
    raise ValueError("The date end is empty")
  else:
    raise ValueError("The date start and end is empty")

  try:
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=0)

  except ValueError:
    raise ValueError("The date must be in the 'YYYY-MM-DD' format.")

  if start_date > end_date:
    raise ValueError("The start date cannot be later than the end date.")

  if end_date < start_date:
    raise ValueError("The end date cannot be earlier than the start date.")

  return [start_date, end_date]
