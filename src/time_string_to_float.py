def time_string_to_float(text):
  hours, minutes = map(int, text.split(":"))
  hour_float = hours + (minutes/60)
  return hour_float
