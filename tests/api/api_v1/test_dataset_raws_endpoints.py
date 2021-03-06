import pytest 
import requests
import random

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api, secure_random, client
from .test_login import client_login
from .test_dataset_inputs_endpoints import get_random_dsi_uuid, create_one_dsi, delete_all_dsi



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### POST NEW DSR
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def create_one_dsr ( 
  as_test = True,
  dsi_uuid = None,
  access_token = None,
  payload = None,
  ) : 

  # server_api = get_server_api()

  ### ACCESS TOKEN
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else : 
    test_user_access_token = access_token
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )

  ### DSI UUID
  if dsi_uuid == None :
    try : 
      test_dsi_uuid = get_random_dsi_uuid( only_test_dsi = True )
    except : 
      test_dsi = create_one_dsi ( as_test = False ) 
      test_dsi_uuid = test_dsi['data']['dsi_uuid']

  else : 
    test_dsi_uuid = dsi_uuid

  ### PAYLOAD
  if payload == None :
    random_int = random.randint(0, 1000) 
    dsr_test_payload = {
      "is_test_data": True,
      "auth_preview": "opendata",
      "auth_modif": "private",
      "data": {
        "field_01": f"test DSR - {random_int}"
      }
    }
  else : 
    dsr_test_payload = payload

  ### REQUEST
  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/create"
  url = f"{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/create"

  # response = requests.post(
  response = client.post(
    url,
    json = dsr_test_payload,
    headers = headers
  )
  resp = response.json() 
  log_.debug ('=== resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


@pytest.mark.create
def test_create_one_dsr(client_access_token):

  test_dsi = create_one_dsi( 
    access_token = client_access_token,
    as_test = False 
  )
  log_.debug ('=== test_dsi : \n%s', pformat(test_dsi) )
  assert test_dsi['data']['is_test_data'] == True

  test_dsi_uuid = test_dsi['data']['dsi_uuid']
  log_.debug ('=== test_dsi_uuid : %s', test_dsi_uuid )

  create_one_dsr( dsi_uuid = test_dsi_uuid )




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET LIST DSRs
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_list_dsr( 
  as_test = True,
  page_number = 1, 
  results_per_page = 100,
  dsi_uuid = None,
  access_token = None
  ):

  # server_api = get_server_api()
  # log_.debug('=== server_api : %s', server_api)

  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else : 
    test_user_access_token = access_token
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )

  if dsi_uuid == None : 
    test_dsi = create_one_dsi ( 
      as_test = False, 
      access_token = test_user_access_token 
    ) 
    assert test_dsi['data']['is_test_data'] == True
    test_dsi_uuid = test_dsi['data']['dsi_uuid']
  else :
    test_dsi_uuid = dsi_uuid

  log_.debug('=== get_list_dsr / test_dsi_uuid : %s', test_dsi_uuid)

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  params = {
    'page_n' : page_number,
    'per_page' : results_per_page
  }

  # url = f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}"
  url = f"{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}"

  # response = requests.get(
  response = client.get(
    url,
    params=params,
    headers=headers
  )
  resp = response.json() 
  log_.debug('=== get_list_dsr / resp : \n%s', pformat(resp) )

  if as_test :
    assert response.status_code == 200 or resp['data'] == []
  else :
    return resp


@pytest.mark.get
def test_get_list_dsr( 
  client_access_token,
  as_test = True,
  test_dsi_uuid = None,
  ) : 

  resp = get_list_dsr( 
    access_token = client_access_token,
    dsi_uuid = test_dsi_uuid,
  )
  log_.debug('=== test_get_list_dsr / resp : \n%s', pformat(resp) )

  if as_test == False :
    return resp




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UTILS DSR
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
### GET ONE DSR
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_one_dsr( 
  as_test = True, 
  only_test_data = False, 
  dsi_uuid = None,
  access_token = None,
  ):

  server_api = get_server_api()
  # log_.debug('=== server_api : %s', server_api)

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else :
    test_user_access_token = access_token
  log_.debug ('=== update_one_dsr / test_user_access_token : %s', test_user_access_token )

  ### get DSI UUID
  if dsi_uuid == None : 
    test_dsi = create_one_dsi ( 
      as_test = False 
    )
    assert test_dsi['data']['is_test_data'] == True
    test_dsi_uuid = test_dsi['data']['dsi_uuid']
  else :
    test_dsi_uuid = dsi_uuid
  log_.debug('=== test_get_one_dsr / test_dsi_uuid : %s', test_dsi_uuid )

  ### get DSR UUID
  test_dsr = create_one_dsr( 
    as_test=False, 
    dsi_uuid=test_dsi_uuid 
  )
  log_.debug('=== test_get_one_dsr / test_dsr : \n%s', pformat(test_dsr) )
  test_dsr_uuid = test_dsr['data']['dsr_uuid']
  log_.debug('=== test_get_one_dsr / test_dsr_uuid : %s', test_dsr_uuid )

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/get_one/{test_dsr_uuid}"
  url = f"{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/get_one/{test_dsr_uuid}"

  ### get DSRs list
  # response = requests.get(
  response = client.get(
    url,
    headers = headers
  )
  resp = response.json()
  log_.debug('=== test_get_one_dsr / resp : \n%s', pformat(resp) )
  
  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


@pytest.mark.get
def test_get_one_dsr(client_access_token):
  get_one_dsr(
    access_token = client_access_token,
  )


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UPDATE DSR
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def update_one_dsr( 
  as_test = True, 
  full_update = False, 
  version_n = None,
  update_data = None,
  dsi_uuid = None,
  dsr_uuid = None,
  access_token = None,
  ): 

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else : 
    test_user_access_token = access_token
  log_.debug ('=== update_one_dsr / test_user_access_token : %s', test_user_access_token )

  ### create a test DSI and DSR
  if dsi_uuid == None and dsr_uuid == None :
    log_.debug ('=== update_one_dsr / no dsi_uuid nor dsr_uuid...')

    test_dsr = create_one_dsr( as_test = False, dsi_uuid=dsi_uuid )
    log_.debug ('=== update_one_dsr / test_dsr : \n%s', pformat(test_dsr) )
    test_dsi_uuid = test_dsr['data']['dsi_uuid']
    test_dsr_uuid = test_dsr['data']['dsr_uuid']
    log_.debug('=== update_one_dsr / test_dsi_uuid : %s', test_dsi_uuid )
    log_.debug('=== update_one_dsr / test_dsr_uuid : %s', test_dsr_uuid )
  
  else : 
    test_dsi_uuid = dsi_uuid

    if dsi_uuid != None and dsr_uuid == None :
      test_dsr = create_one_dsr( as_test = False, dsi_uuid=dsi_uuid )
      test_dsr_uuid = test_dsr['data']['dsr_uuid']
    else :
      test_dsr_uuid = dsr_uuid

  ### mockup update field
  if update_data == None :
    random_int = random.randint(0, 1000) 
    update_data = {
      "update_data" : {

        'source' : f'my new source - {random_int}',
        'licence' : 'Obbl-42',
        "auth_preview": "commons",
        "auth_modif": "team",
        "data" : {
          "field_01": f"this is updated data on field_01 - {random_int}",
          "field_02": f"my updated field_02 data - {random_int}",
          "field_03": {
            "subfield_A": f"Update data for numerical or text... {random_int}",
            "subfield_B": random_int
          }
        }
      }
    }

  params_update = {
    'full_update' : full_update,
    'version_n' : version_n
  }

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/update/{test_dsr_uuid}"
  url = f"{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/update/{test_dsr_uuid}"

  ### update doc
  # response = requests.put(
  response = client.put(
    url,
    json = update_data,
    params = params_update,
    headers = headers
  )
  resp = response.json() 
  log_.debug ('=== update_one_dsr / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
    for key in update_data['update_data'].keys() :
      if key != 'data' : 
        assert resp['data'][key] == update_data['update_data'][key]
    for key in update_data['update_data']['data'].keys() :
      assert resp['data']['data'][key] == update_data['update_data']['data'][key]
  else : 
    return resp


@pytest.mark.update
def test_update_one_dsr_no_full_update(client_access_token) :
  update_one_dsr(
    access_token = client_access_token,
    full_update = False 
  )

@pytest.mark.update
def test_update_one_dsr_no_full_update_with_data(client_access_token) :

  random_int = random.randint(0, 1000) 

  # test_user_access_token = client_login( as_test = False, only_access_token=True )
  test_user_access_token = client_access_token

  update_data_one = {
    "update_data" : {
      "data" : {
        "field_01": f"my data field_01 data +BIS+ - {random_int}",
        "field_02": f"my data field_02 data +BIS+ - {random_int}",
        "field_03": f"my data field_03 data +BIS+ - {random_int}",
      }
    }
  }

  resp_one = update_one_dsr(
    as_test = False,
    update_data = update_data_one,
    full_update = False,
    access_token = test_user_access_token
  )
  log_.debug ('=== test_update_one_dsr_no_full_update_with_data / resp_one : \n%s', pformat(resp_one) )
  dsi_uuid = resp_one['data']['dsi_uuid']
  dsr_uuid = resp_one['data']['dsr_uuid']

  update_data_bis = {
    "update_data" : {
      "data" : {
        "field_02": f"my updated field_02 data +BIS+ - {random_int + 1}",
      }
    }
  }
  resp_bis = update_one_dsr(
    # as_test = False,
    full_update = False, 
    update_data = update_data_bis,
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    access_token = test_user_access_token
  )
  # log_.debug ('=== test_update_one_dsr_no_full_update_with_data / resp_one : \n%s', pformat(resp_one) )
  # log_.debug ('=== test_update_one_dsr_no_full_update_with_data / resp_bis : \n%s', pformat(resp_bis) )

@pytest.mark.update
def test_update_one_dsr_full_update(client_access_token) :

  random_int = random.randint(0, 1000) 
  update_data = {
    "update_data" : {
      "data" : {
        "field_01": f"this is +full_update+ updated data on field_01 - {random_int}",
        "field_42": f"this is +full_update+ updated data on field_42 - {random_int}",
      }
    }
  }
  update_one_dsr( 
    access_token = client_access_token,
    full_update = True,
    update_data = update_data
  )






### - - - - - - - - - - - - - - - - - - - - - - - ### 
### DELETE DSR
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def delete_one_dsr (
  as_test = True, 
  server_api = None,
  access_token = None,
  full_remove = False,
  dsi_uuid = None 
  ) :

  if server_api == None :
    server_api = get_server_api()

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
    log_.debug ('=== delete_one_dsr / test_user_access_token : %s', test_user_access_token )
  else :
    test_user_access_token = access_token

  ### get DSI uuid
  if dsi_uuid == None :
    test_dsi = create_one_dsi ( as_test = False ) 
    assert test_dsi['data']['is_test_data'] == True
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
    'full_remove' : full_remove,
  }
  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/remove/{test_dsr_uuid}"
  url = f"{config.API_V1_STR}/crud/dataset/{test_dsi_uuid}/dsr/remove/{test_dsr_uuid}"

  # response = requests.delete(
  response = client.delete(
    url,
    params = params_delete,
    headers = headers
  )
  log_.debug ('=== delete_one_dsr / response : \n%s', pformat(response) )

  if as_test : 
    assert response.status_code == 200
  else : 
    resp = response.json()
    return resp


@pytest.mark.delete
def test_delete_dsr_no_full_remove(client_access_token):

  dsi_uuid = None 
  delete_one_dsr(
    access_token = client_access_token,
    dsi_uuid = dsi_uuid,
    full_remove = False 
  )

@pytest.mark.delete
def test_delete_dsr_full_remove(client_access_token):

  dsi_uuid = None 
  delete_one_dsr( 
    access_token = client_access_token,
    dsi_uuid = dsi_uuid,
    full_remove = True,
  )




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### CLEANUP DSRs
### - - - - - - - - - - - - - - - - - - - - - - - ### 

### clean up all test DSRs and DSIs

@pytest.mark.delete
def test_delete_all_test_dsr_dsi(client_access_token):
  delete_all_dsi( 
    access_token = client_access_token,
    only_test_data = True,
    full_remove = True 
  )