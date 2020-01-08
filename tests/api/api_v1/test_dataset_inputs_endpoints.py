import requests
import random
secure_random = random.SystemRandom()

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api
from .test_login import *




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET LIST
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_get_list_dsi( 
  as_test = True, 
  page_number=1, 
  results_per_page=100 
  ):

  server_api = get_server_api()
  # log_.debug('=== server_api : %s', server_api)

  params = {
    'page_n' : page_number,
    'per_page' : results_per_page
  }

  response = requests.get(
    f"{server_api}{config.API_V1_STR}/dsi/list",
    params=params
  )
  resp = response.json()
  # log_.debug ('=== resp : \n%s', pformat(resp) )

  if as_test : 
    log_.debug ('=== resp : \n%s', pformat(resp) )
    assert response.status_code == 200
  else :
    return resp



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### POST
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_create_one_dsi( as_test = True ):

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  test_user_access_token = test_client_login( as_test = False, only_access_token=True )
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )

  random_int = random.randint(0, 1000) 

  dsi_test_payload = {
    "title": f"my test DSI - {random_int}",
    "description": "my DSI description",
    "licence": "MIT",
    "is_geodata": False,
    "auth_preview": "opendata",
    "auth_modif": "private",
    "is_test_data" : True
  }

  response = requests.post(
    f"{server_api}{config.API_V1_STR}/dsi/create",
    json = dsi_test_payload,
    headers = {
      'accept': 'application/json',
      'access_token' : test_user_access_token,
    }
  )
  resp = response.json() 
  log_.debug ('=== resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp



def get_random_dsi_uuid( only_test_dsi = False ) : 

  test_dsi_list = test_get_list_dsi( as_test = False )
  full_dsi_list = test_dsi_list['data']
  if only_test_dsi : 
    testable_dsi = [ i for i in full_dsi_list if i['is_test_data'] == True ]
    test_dsi = secure_random.choice( testable_dsi )
  else :
    test_dsi = secure_random.choice( full_dsi_list )
  test_dsi_uuid = test_dsi['dsi_uuid']
  log_.debug ('=== test_dsi_uuid : %s', test_dsi_uuid)
  return test_dsi_uuid



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET ONE
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_get_one_dsi( as_test = True, only_test_data = False ):
  server_api = get_server_api()
  log_.debug ('=== server_api : %s', server_api)

  # test_dsi_uuid = '3ffbacf768f1481cb2b8968381490a72'
  test_dsi_uuid = get_random_dsi_uuid( only_test_dsi = only_test_data ) 
  log_.debug ('=== test_dsi_uuid : %s', test_dsi_uuid)

  response = requests.get(
    f"{server_api}{config.API_V1_STR}/dsi/get_one/{test_dsi_uuid}"
  )
  resp = response.json()
  log_.debug ('=== resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


def test_get_one_dsi_test(): 
  try :
    test_get_one_dsi( only_test_data = True )
  except : 
    log_.debug ('=== no test DSI ...' )
    assert False




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### DELETE
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def delete_dsi( 
  as_test = True, 
  only_test_data = True,
  full_remove = False
  ): 

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### get test user
  test_user_access_token = test_client_login( as_test = False, only_access_token=True )
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )

  ### get list of DSIs
  test_dsi_list = test_get_list_dsi( as_test = False )
  full_dsi_list = test_dsi_list['data']

  if only_test_data : 
    testable_dsi_list = [ i for i in full_dsi_list if i['is_test_data'] == True ]
  else : 
    testable_dsi_list = full_dsi_list

  # log_.debug ('=== testable_dsi_list : \n%s', pformat(testable_dsi_list) )

  ### delete list of DSIs
  for dsi in testable_dsi_list : 

    # log_.debug ('=== dsi : \n%s', pformat(dsi) )

    dsi_uuid = dsi['dsi_uuid']
    log_.debug ('=== dsi_uuid : %s', dsi_uuid )
    
    params_delete = {
      # 'dsi_uuid' : dsi_uuid ,
      'full_remove' : full_remove,
    }
    headers = {
      'accept': 'application/json',
      'access_token' : test_user_access_token,
    }

    response = requests.delete(
      f"{server_api}{config.API_V1_STR}/dsi/remove/{dsi_uuid}",
      params = params_delete,
      headers = headers
    )
    assert response.status_code == 200 


def test_delete_dsi_no_full_remove(): 
  delete_dsi( full_remove=False )


def test_delete_dsi_full_remove(): 
  delete_dsi( full_remove=True )