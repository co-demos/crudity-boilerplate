from pprint import pprint, pformat

import os
# from datetime import time

import logging
from logging.config import dictConfig

import colorlog
from colorlog import ColoredFormatter


# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
# print (" loggers : \n %s" , pformat(loggers) )
# existing_logger_names = logging.getLogger().manager.loggerDict.keys()
# print ("... existing_logger_names : \n" , pformat(existing_logger_names) )

# cf : https://stackoverflow.com/questions/17668633/what-is-the-point-of-setlevel-in-a-python-logging-handler

APP_MODE = os.getenv("APP_MODE", "default")

### log files
LOGS_FOLDER=os.getenv("LOGS_FOLDER", '_logs')
LOGS_FILE_INFOS=os.getenv("LOGS_FILE_INFOS", 'infos_logs.log')
LOGS_FILE_WARNINGS=os.getenv("LOGS_FILE_WARNINGS", "warning_logs.log")
LOGS_FILE_ERRORS=os.getenv("LOGS_FILE_ERRORS", "error_logs.log")
LOGS_FILE_CRITICALS=os.getenv("LOGS_FILE_CRITICALS", "critical_logs.log")

LOGS_TO_FILE_LEVELS=os.getenv("LOGS_TO_FILE_LEVELS", 'E,C')
LOGS_TO_FILE_LEVELS = LOGS_TO_FILE_LEVELS.split(",")
print ("LOGS_TO_FILE_LEVELS" , LOGS_TO_FILE_LEVELS)

## create a formatter for future logger
formatter = ColoredFormatter(
  "%(log_color)s%(levelname)1.1s ::: %(name)s %(asctime)s ::: %(module)s:%(lineno)d -in- %(funcName)s ::: %(reset)s %(white)s%(message)s",
  datefmt='%y-%m-%d %H:%M:%S',
  reset=True,
  log_colors={
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red,bg_white',
  },
  secondary_log_colors={},
  style='%'
)

### create handler
handler = colorlog.StreamHandler()
handler.setFormatter(formatter)

### create logger
log_ = colorlog.getLogger()
# print ("log_ :", log_.__dict__)
if ( log_.hasHandlers() ):
  log_.handlers.clear()
log_.addHandler(handler)

### set logging level
log_.setLevel(logging.DEBUG)

if 'I' in LOGS_TO_FILE_LEVELS : 

  log_file_I = logging.handlers.RotatingFileHandler(f'{LOGS_FOLDER}/{LOGS_FILE_INFOS}')
  log_file_I.setFormatter(formatter)
  log_file_I.setLevel(logging.INFO)
  log_.addHandler(log_file_I)

if 'W' in LOGS_TO_FILE_LEVELS : 

  log_file_W = logging.handlers.RotatingFileHandler(f'{LOGS_FOLDER}/{LOGS_FILE_WARNINGS}')
  log_file_W.setFormatter(formatter)
  log_file_W.setLevel(logging.INFO)
  log_.addHandler(log_file_W)

if 'E' in LOGS_TO_FILE_LEVELS : 

  log_file_E = logging.handlers.RotatingFileHandler(f'{LOGS_FOLDER}/{LOGS_FILE_ERRORS}')
  log_file_E.setFormatter(formatter)
  log_file_E.setLevel(logging.ERROR)
  log_.addHandler(log_file_E)

if 'C' in LOGS_TO_FILE_LEVELS : 

  log_file_C = logging.handlers.RotatingFileHandler(f'{LOGS_FOLDER}/{LOGS_FILE_CRITICALS}')
  log_file_C.setFormatter(formatter)
  log_file_C.setLevel(logging.CRITICAL)
  log_.addHandler(log_file_C)





# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# formatter.converter = time.gmtime

# console_handler = logging.StreamHandler()

# if APP_MODE == "production":
#   console_handler.setLevel(logging.ERROR)
# else:
#   console_handler.setLevel(level)

# console_handler.setFormatter(formatter)

# handlers = [console_handler]

# if APP_MODE == "production":
#   error_handler = logging.FileHandler("app_error.log")
#   error_handler.setLevel(logging.ERROR)
#   error_handler.setFormatter(formatter)
#   handlers.append(error_handler)

# logging.basicConfig(handlers=handlers)