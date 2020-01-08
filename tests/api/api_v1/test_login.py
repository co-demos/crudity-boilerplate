import requests
from log_config import log_, pformat
from starlette.testclient import TestClient

from main import app
from core import config
from tests.utils.utils import get_server_api

client = TestClient(app)
# log_.debug("=== client : %s", client)


### cf : https://fastapi.tiangolo.com/tutorial/testing/

def test_client_anonymous_login( as_test = True ):

  server_api = get_server_api()
  # log_.debug("=== server_api : %s", server_api)
  response = requests.get(
    f"{server_api}{config.API_V1_STR}/anonymous_login"
  )
  resp = response.json()
  # log_.debug("=== resp : \n%s", pformat( resp ))

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


def test_client_login( as_test = True, only_access_token = False ):

  server_api = get_server_api()

  ### get ano access token
  # response_ano = requests.get(
  #   f"{server_api}{config.API_V1_STR}/anonymous_login"
  # )
  # response_ano_json = response_ano.json()
  response_ano_json = test_client_anonymous_login( as_test=False )
  # log_.debug("=== response_ano_json : \n%s", pformat( response_ano_json ))

  response_ano_access_token = response_ano_json['tokens']['access_token']
  # log_.debug("=== response_ano_access_token : %s", response_ano_access_token )

  ### log test user
  login_test = {
    "user_login": {
      "email": "ostrom@emailna.co",
      "password": "a-very-common-password"
    }
  }
  response = requests.post(
    f"{server_api}{config.API_V1_STR}/login",
    json = login_test,
    headers = { 
      'accept': 'application/json',
      'access_token' : response_ano_access_token 
    }
  )
  # log_.debug("=== response : \n%s", pformat(response.json() ) )
  resp = response.json()

  if as_test : 
    assert response.status_code == 200 
    assert resp['tokens']['access_token']
  else :
    if only_access_token : 
      return resp['tokens']['access_token']
    else :
      return resp