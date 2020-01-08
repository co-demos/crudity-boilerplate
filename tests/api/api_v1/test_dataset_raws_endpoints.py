import requests
import random
secure_random = random.SystemRandom()

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api
from .test_dataset_inputs_endpoints import get_random_dsi_uuid
from .test_login import *


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET LIST
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_get_list_dsr( as_test = True ):
  server_api = get_server_api()

  # log_.debug('=== server_api : %s', server_api)
  # test_dsi_uuid = '3ffbacf768f1481cb2b8968381490a72'
  test_dsi_uuid = get_random_dsi_uuid()
  log_.debug('=== test_dsi_uuid : %s', test_dsi_uuid)

  response = requests.get(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}"
  )
  resp = response.json()
  # log_.debug('=== resp : \n%s', pformat(resp) )

  if as_test :
    assert response.status_code == 200
  else :
    return resp


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET ONE
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_get_one_dsr( as_test = True, only_test_data = False ):

  server_api = get_server_api()

  # log_.debug('=== server_api : %s', server_api)
  # test_dsi_uuid = '3ffbacf768f1481cb2b8968381490a72'
  test_dsi_uuid = get_random_dsi_uuid()

  test_dsr_uuid = '3ffbacf768f1481cb2b8968381490a72'




  response = requests.get(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/get_one/{test_dsr_uuid}"
  )
  resp = response.json()
  # log_.debug('=== resp : \n%s', pformat(resp) )
  assert response.status_code == 200




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### `POST
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_create_one_dsr ( as_test = True ) : 

  server_api = get_server_api()
  test_user_access_token = test_client_login( as_test = False, only_access_token=True )
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )
  
  test_dsi_uuid = get_random_dsi_uuid( only_test_dsi = True )

  random_int = random.randint(0, 1000) 

  dsr_test_payload = {
    "data": {
      "field_01": f"test DSR - {random_int}"
    }
  }

  response = requests.post(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/create"
    json = dsr_test_payload,
    headers = {
      'accept': 'application/json',
      'access_token' : test_user_access_token,
    }
  )
  resp = response.json() 
  log_.debug ('=== resp : \n%s', pformat(resp) )



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### DELETE
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_delete_one_dsr (as_test = True) :
  server_api = get_server_api()
  test_user_access_token = test_client_login( as_test = False, only_access_token=True )
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )
