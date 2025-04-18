from datetime import datetime, timedelta
from pytz import timezone
from . import getenv


def get_last_half_hour(every_minutes=5, last_minutes=30) -> list:
  now = datetime.now(timezone(getenv("TIMEZONE")))

  minutes = (now.minute // every_minutes) * every_minutes
  last_half_hour_start = now.replace(minute=minutes, second=0, microsecond=0) - timedelta(minutes=last_minutes)

  time_slots = []
  for i in range(0, (last_minutes + 1), 5):
    time_slot = (last_half_hour_start + timedelta(minutes=i)).strftime('%H:%M')
    time_slots.append(time_slot)

  return time_slots
