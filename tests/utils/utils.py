import requests

import random
import string 

from log_config import log_, pformat
from starlette.testclient import TestClient

from main import app
from core import config

client = TestClient(app)
secure_random = random.SystemRandom()

### cf : https://fastapi.tiangolo.com/tutorial/testing/



def random_lower_string():
  return "".join(random.choices(string.ascii_lowercase, k=32))


def get_server_api():
  server_name = f"http://{config.SERVER_NAME}"
  return server_name