def get_field_list(fields_list, index, default, transform=lambda x: x):
  try:
    return transform(fields_list[index])
  except IndexError:
    return default
  except Exception:
    return default
