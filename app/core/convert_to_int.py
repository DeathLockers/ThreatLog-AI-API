def convert_to_int(val, default_val=0):
  try:
    return int(val)
  except ValueError:
    return default_val
