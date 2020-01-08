import requests
import random
secure_random = random.SystemRandom()

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api
from .test_dataset_inputs_endpoints import get_random_dsi_uuid, create_one_dsi, delete_all_dsi
from .test_login import client_login




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### POST
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def create_one_dsr ( 
  as_test = True,
  dsi_uuid = None
  ) : 

  server_api = get_server_api()
  test_user_access_token = client_login( as_test = False, only_access_token=True )
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )
  
  if dsi_uuid == None :
    test_dsi_uuid = get_random_dsi_uuid( only_test_dsi = True )
  else : 
    test_dsi_uuid = dsi_uuid

  random_int = random.randint(0, 1000) 

  dsr_test_payload = {
    "data": {
      "field_01": f"test DSR - {random_int}"
    }
  }

  response = requests.post(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/create",
    json = dsr_test_payload,
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


def test_create_one_dsr():

  test_dsi = create_one_dsi( as_test=False )
  log_.debug ('=== test_dsi : \n%s', pformat(test_dsi) )

  test_dsi_uuid = test_dsi['data']['dsi_uuid']
  log_.debug ('=== test_dsi_uuid : %s', test_dsi_uuid )

  create_one_dsr( dsi_uuid = test_dsi_uuid )


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET LIST
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_list_dsr( 
  as_test = True,
  page_number=1, 
  results_per_page=100,
  dsi_uuid = None
  ):

  server_api = get_server_api()
  # log_.debug('=== server_api : %s', server_api)

  if dsi_uuid == None : 
    test_dsi = create_one_dsi ( as_test = False ) 
    test_dsi_uuid = test_dsi['data']['dsi_uuid']
  else :
    test_dsi_uuid = dsi_uuid

  log_.debug('=== get_list_dsr / test_dsi_uuid : %s', test_dsi_uuid)

  params = {
    'page_n' : page_number,
    'per_page' : results_per_page
  }

  response = requests.get(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}",
    params=params
  )
  resp = response.json() 
  log_.debug('=== get_list_dsr / resp : \n%s', pformat(resp) )

  if as_test :
    assert response.status_code == 200 or resp['data'] == []
  else :
    return resp


def test_get_list_dsr( 
  as_test = True,
  test_dsi_uuid = None
  ) : 

  resp = get_list_dsr( dsi_uuid = test_dsi_uuid )
  log_.debug('=== test_get_list_dsr / resp : \n%s', pformat(resp) )

  if as_test == False :
    return resp



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UTILS
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_random_dsr_uuid( 
  dsi_uuid = None,
  only_test_dsr = False
  ) : 

  test_dsr_list = get_list_dsr( 
    as_test = False, 
    dsi_uuid = dsi_uuid
  )
  log_.debug ('=== get_random_dsr_uuid / test_dsr_list : \n%s', pformat(test_dsr_list))

  full_dsr_list = test_dsr_list['data']

  if only_test_dsr : 
    testable_dsi = [ i for i in full_dsr_list if i['is_test_data'] == True ]
    test_dsr = secure_random.choice( testable_dsi )
  else :
    test_dsr = secure_random.choice( full_dsr_list )

  log_.debug ('=== get_random_dsr_uuid / test_dsr : \n%s', pformat(test_dsr))

  test_dsr_uuid = test_dsr['_source']['dsr_uuid']
  log_.debug ('=== get_random_dsr_uuid / test_dsr_uuid : %s', test_dsr_uuid)

  return test_dsr_uuid



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET ONE
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def test_get_one_dsr( 
  as_test = True, 
  only_test_data = False, 
  dsi_uuid = None
  ):

  server_api = get_server_api()
  # log_.debug('=== server_api : %s', server_api)

  ### get DSI UUID
  if dsi_uuid == None : 
    test_dsi = create_one_dsi ( as_test = False ) 
    test_dsi_uuid = test_dsi['data']['dsi_uuid']
  else :
    test_dsi_uuid = dsi_uuid
  log_.debug('=== test_dsi_uuid : %s', test_dsi_uuid )

  ### get DSR UUID
  test_dsr = create_one_dsr( as_test=False, dsi_uuid=test_dsi_uuid )
  log_.debug('=== test_dsr : \n%s', pformat(test_dsr) )
  test_dsr_uuid = test_dsr['data']['dsr_uuid']
  log_.debug('=== test_dsr_uuid : %s', test_dsr_uuid )

  ### get DSRs list
  response = requests.get(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/get_one/{test_dsr_uuid}"
  )
  resp = response.json()
  log_.debug('=== resp : \n%s', pformat(resp) )
  
  if as_test : 
    assert response.status_code == 200
  else : 
    return resp



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### DELETE
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def delete_one_dsr (
  as_test = True, 
  only_test_data = True,
  full_remove = False,
  dsi_uuid = None 
  ) :

  server_api = get_server_api()

  test_user_access_token = client_login( as_test = False, only_access_token=True )
  log_.debug ('=== delete_one_dsr / test_user_access_token : %s', test_user_access_token )

  if dsi_uuid == None :
    test_dsi = create_one_dsi ( as_test = False ) 
    test_dsi_uuid = test_dsi['data']['dsi_uuid']
    test_dsr_01 = create_one_dsr( as_test=False, dsi_uuid=test_dsi_uuid )
    log_.debug('=== delete_one_dsr / test_dsr_01 : \n%s', pformat(test_dsr_01) )
    # test_dsr_02 = create_one_dsr( as_test=False, dsi_uuid=test_dsi_uuid )
    # test_dsr_03 = create_one_dsr( as_test=False, dsi_uuid=test_dsi_uuid )
    test_dsr_uuid = test_dsr_01['data']['dsr_uuid']

  else : 
    test_dsi_uuid = dsi_uuid
    test_dsr_list = get_list_dsr( dsi_uuid=test_dsi_uuid )
    log_.debug('=== delete_one_dsr / test_dsr_list : \n%s', pformat(test_dsr_list) )
    test_dsr_uuid = get_random_dsr_uuid( dsi_uuid=test_dsi_uuid )

  log_.debug('=== delete_one_dsr / test_dsi_uuid : %s', test_dsi_uuid )
  log_.debug('=== delete_one_dsr / test_dsr_uuid : %s', test_dsr_uuid )

  params_delete = {
    # 'dsi_uuid' : dsi_uuid ,
    'full_remove' : full_remove,
  }
  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  response = requests.delete(
    f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/remove/{test_dsr_uuid}",
    params = params_delete,
    headers = headers
  )
  resp = response.json()
  log_.debug ('=== delete_one_dsr / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


def test_delete_dsr_no_full_remove():

  # dsi_uuid = 'c6dc3cd0904a4090a75be94033a574c7'
  dsi_uuid = None 

  delete_one_dsr(
    dsi_uuid = dsi_uuid,
  )


def test_delete_dsr_full_remove():

  # dsi_uuid = 'c6dc3cd0904a4090a75be94033a574c7'
  dsi_uuid = None 

  delete_one_dsr( 
    dsi_uuid = dsi_uuid,
    full_remove = True 
  )


### clean up all that
def test_delete_all_test_dsr_dsi():
  delete_all_dsi( full_remove=True )