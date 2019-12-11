from log_config import log_, pformat

import uuid
from core import config

log_.debug(">>> crud/utils.py")

def generate_new_id():
  return str(uuid.uuid4())