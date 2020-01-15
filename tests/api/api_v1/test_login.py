import pytest
import requests

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api, client





### - - - - - - - - - - - - - - - - - - - - - - - ### 
### LOGINS 
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def client_anonymous_login( 
  as_test = True,
  only_access_token = False,
  ):

  # server_api = get_server_api()
  # log_.debug("=== client_anonymous_login / server_api : %s", server_api)

  # url = f"{server_api}{config.API_V1_STR}/anonymous_login"
  url = f"{config.API_V1_STR}/anonymous_login"
  
  # log_.debug("=== url : %s", url)

  # response = requests.get(
  response = client.get(
    url,
  )
  resp = response.json()
  # log_.debug("=== client_anonymous_login / resp : \n%s", pformat( resp ))

  if as_test : 
    assert response.status_code == 200
  else : 
    if only_access_token : 
      return resp['tokens']['access_token']
    else :
      return resp

@pytest.mark.user
def test_client_anonymous_login():
  client_anonymous_login() 



def client_login( 
  as_test = True, 
  only_access_token = False 
  ):

  # server_api = get_server_api()

  ### get ano access token
  response_ano_json = client_anonymous_login( as_test=False )
  # log_.debug("=== client_login / response_ano_json : \n%s", pformat( response_ano_json ))

  response_ano_access_token = response_ano_json['tokens']['access_token']
  # log_.debug("=== client_login / response_ano_access_token : %s", response_ano_access_token )

  ### log test user
  login_test = {
    "user_login": {
      "email": "ostrom@emailna.co",
      "password": "a-very-common-password"
    }
  }

  # url = f"{server_api}{config.API_V1_STR}/login"
  url = f"{config.API_V1_STR}/login"

  # response = requests.post(
  response = client.post(
    url,
    json = login_test,
    headers = { 
      'accept': 'application/json',
      'access_token' : response_ano_access_token 
    }
  )
  # log_.debug("=== client_login / response : \n%s", pformat(response.json() ) )
  resp = response.json()

  if as_test : 
    assert response.status_code == 200 
    assert resp['tokens']['access_token']
  else :
    if only_access_token : 
      return resp['tokens']['access_token']
    else :
      return resp

@pytest.mark.user
def test_client_login() :
  client_login()




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### REGISTER - TO DO 
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def client_register( 
  as_test = True 
  ):

  response_ano_json = client_anonymous_login( as_test=False )
  response_ano_access_token = response_ano_json['tokens']['access_token']

  register_test = {
    "user_register": {
      "name": "Elinor",
      "surname": "Ostrom",
      "email": "ostrom@emailna.co",
      "password": "a-very-common-password",
    }
  }

  url = f"{config.API_V1_STR}/register"

  response = client.post(
    url,
    json = login_test,
    headers = { 
      'accept': 'application/json',
      'access_token' : response_ano_access_token 
    }
  )
  log_.debug("=== client_register / response : \n%s", pformat(response.json() ) )
  resp = response.json()

  if as_test : 
    log_.debug ('=== client_register / resp : \n%s', pformat(resp) )
    assert response.status_code == 200 
    assert resp['tokens']['access_token']
  else :
    return resp


@pytest.mark.user
@pytest.mark.skip(reason='not developped yet')
def test_client_register():
  client_register()