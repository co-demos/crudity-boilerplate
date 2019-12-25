import requests

from core import config
from tests.utils.utils import get_server_api

def test_get_list_dsr():
  server_api = get_server_api()
  print ('=== server_api : ', server_api)
  test_dsi_uuid = '3ffbacf768f1481cb2b8968381490a72'
  response = requests.get(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}"
  )
  assert response.status_code == 200