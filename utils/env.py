import os 

def get_boolean(value):
  result = False
  if value is not None:
    result = value.upper() in ("TRUE", "1")
  return result

def getenv_boolean(var_name, default_value=False):
  result = default_value
  env_value = os.getenv(var_name)
  result = get_boolean(env_value)
  # if env_value is not None:
  #   result = env_value.upper() in ("TRUE", "1")
  return result