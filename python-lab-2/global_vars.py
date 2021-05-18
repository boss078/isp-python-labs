def init(global_variables):
  for key, value in global_variables.items():
    globals()[key] = value
