import requests
import random
secure_random = random.SystemRandom()

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api
from .test_login import client_login




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET LIST DSIs
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
### POST NEW DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def create_one_dsi( as_test = True ):

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  test_user_access_token = client_login( as_test = False, only_access_token=True )
  log_.debug ('=== create_one_dsi / test_user_access_token : %s', test_user_access_token )

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
  log_.debug ('=== create_one_dsi / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


def test_create_one_dsi( as_test = True ):
  create_one_dsi( as_test = as_test )
  

### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET ONE DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_random_dsi_uuid( only_test_dsi = False ) : 

  test_dsi_list = test_get_list_dsi( as_test = False )
  full_dsi_list = test_dsi_list['data']
  if only_test_dsi : 
    testable_dsi = [ i for i in full_dsi_list if i['is_test_data'] == True ]
    test_dsi = secure_random.choice( testable_dsi )
  else :
    test_dsi = secure_random.choice( full_dsi_list )
  test_dsi_uuid = test_dsi['dsi_uuid']
  log_.debug ('=== get_random_dsi_uuid / test_dsi_uuid : %s', test_dsi_uuid)
  return test_dsi_uuid


def test_get_one_dsi( as_test = True, only_test_data = False ):

  server_api = get_server_api()
  log_.debug ('=== test_get_one_dsi / server_api : %s', server_api)

  # test_dsi_uuid = '3ffbacf768f1481cb2b8968381490a72'
  test_dsi_uuid = get_random_dsi_uuid( only_test_dsi = only_test_data ) 
  log_.debug ('=== test_get_one_dsi / test_dsi_uuid : %s', test_dsi_uuid)

  response = requests.get(
    f"{server_api}{config.API_V1_STR}/dsi/get_one/{test_dsi_uuid}"
  )
  resp = response.json()
  log_.debug ('=== test_get_one_dsi / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


# def test_get_one_dsi_test(): 
#   try :
#     test_get_one_dsi( only_test_data = True )
#   except : 
#     log_.debug ('=== no test DSI ...' )
#     assert False



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UPDATE DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def update_one_dsi( as_test = True, full_update = False ): 

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### get test user
  test_user_access_token = client_login( as_test = False, only_access_token=True )
  log_.debug ('=== test_update_one_dsi / test_user_access_token : %s', test_user_access_token )

  ### create a test DSI
  test_dsi = create_one_dsi( as_test = False )
  log_.debug ('=== test_update_one_dsi / test_dsi : \n%s', pformat(test_dsi) )

  ### mockup update field
  update_data = {
    "licence" : "my-test-licence",
    "auth_preview" : "private"
  }

  params_update = {
    'full_update' : full_update,
  }

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  ### update doc
  response = requests.put(
    f"{server_api}{config.API_V1_STR}/dsi/create",
    json = update_data,
    params = params_update,
    headers = headers
  )
  resp = response.json() 
  log_.debug ('=== test_update_one_dsi / resp : \n%s', pformat(resp) )

  if as_test : 
    assert resp['data']['licence'] == update_data['licence']
    assert resp['data']['licence'] == update_data['licence']
    assert response.status_code == 200
  else : 
    return resp


def test_update_one_dsi_no_full_update() :
  update_one_dsi()

def test_update_one_dsi_full_update() :
  update_one_dsi( full_update=True )



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### DELETE DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def delete_one_dsi( 
  as_test = True,
  server_api=None,
  dsi_uuid = None, 
  access_token = None,
  full_remove = False,
  ):

  if server_api == None :
    server_api = get_server_api()
    # log_.debug ('=== server_api : %s', server_api)

  if dsi_uuid == None : 
    test_dsi = create_one_dsi( as_test = False ) 
    dsi_uuid = test_dsi['data']['dsi_uuid']

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
    log_.debug ('=== test_user_access_token : %s', test_user_access_token )

  params_delete = {
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




def delete_all_dsi( 
  as_test = True, 
  only_test_data = True,
  full_remove = False,
  ): 

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### get test user
  test_user_access_token = client_login( as_test = False, only_access_token=True )
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
    


    # params_delete = {
    #   # 'dsi_uuid' : dsi_uuid ,
    #   'full_remove' : full_remove,
    # }
    # headers = {
    #   'accept': 'application/json',
    #   'access_token' : test_user_access_token,
    # }

    # response = requests.delete(
    #   f"{server_api}{config.API_V1_STR}/dsi/remove/{dsi_uuid}",
    #   params = params_delete,
    #   headers = headers
    # )
    response = delete_one_dsi( 
      as_test=False, 
      server_api=server_api,
      dsi_uuid=dsi_uuid,
      access_token=test_user_access_token,
      full_remove=full_remove
    )

    assert response.status_code == 200 


def test_delete_dsi_no_full_remove(): 
  delete_all_dsi( full_remove=False )


def test_delete_dsi_full_remove(): 
  delete_all_dsi( full_remove=True )