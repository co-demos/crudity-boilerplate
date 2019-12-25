import requests

from core import config
from tests.utils.utils import get_server_api

def test_get_list_dsi():
  server_api = get_server_api()
  print ('=== server_api : ', server_api)
  response = requests.get(
    f"{server_api}{config.API_V1_STR}/dsi/list"
  )
  assert response.status_code == 200