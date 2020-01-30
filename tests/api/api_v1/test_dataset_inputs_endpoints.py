import pytest
import requests
import random

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api, secure_random, client
from .test_login import client_login




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### POST NEW DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def create_one_dsi( 
  as_test = True,
  access_token = None,
  payload = None,
  ):

  # server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### ACCESS TOKEN
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else : 
    test_user_access_token = access_token
  log_.debug ('=== create_one_dsi / test_user_access_token : %s', test_user_access_token )

  ### PAYLOAD
  if payload == None :
    random_int = random.randint(0, 1000) 
    dsi_test_payload = {
      "title": f"my test DSI - test {random_int}",
      "description": "my DSI description - test {random_int}",
      "licence": "MIT",
      "is_geodata": False,
      "auth_preview": "opendata",
      "auth_modif": "private",
      "is_test_data" : True
    }
  else : 
    dsi_test_payload = payload

  ### REQUEST
  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/dsi/create"
  url = f"{config.API_V1_STR}/dsi/create"

  # response = requests.post(
  response = client.post(
    url,
    json = dsi_test_payload,
    headers = headers
  )
  resp = response.json() 
  log_.debug ('=== create_one_dsi / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


@pytest.mark.create
def test_create_one_dsi( 
  client_access_token,
  as_test = True 
  ):
  create_one_dsi( 
    access_token = client_access_token,
    as_test = as_test 
  )
  

def create_dsi_payload(

  index_int = None,

  title_content = "",
  description_content = "",
  licence = "MIT",
  is_geodata = False,
  auth_preview = "opendata",
  auth_modif = "private",

  ):

  if index_int == None : 
    index_int = random.randint(0, 1000) 

  dsi_test_payload = {

    "title": f"my test DSI - test {index_int} - {title_content}",
    "description": "my DSI description - test {index_int} - {description_content}",

    "licence": licence,
    "is_geodata": is_geodata,
    "auth_preview": auth_preview,
    "auth_modif": auth_modif,

    "is_test_data" : True
  }
  return dsi_test_payload


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET LIST DSIs
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_list_dsi( 
  as_test = True, 
  page_number = 1, 
  results_per_page = 100, 
  access_token = None,
  params = None,
  ):

  # server_api = get_server_api()
  # log_.debug('=== get_list_dsi / server_api : %s', server_api)

  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else : 
    test_user_access_token = access_token
  log_.debug ('=== test_user_access_token : %s', test_user_access_token )

  if params == None :
    params = {
      'page_n' : page_number,
      'per_page' : results_per_page
    }

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/dsi/list",
  url = f"{config.API_V1_STR}/dsi/list"

  # response = requests.get(
  response = client.get(
    url,
    params=params, 
    headers=headers
  )
  resp = response.json()
  # log_.debug ('=== resp : \n%s', pformat(resp) )

  if as_test : 
    log_.debug ('=== get_list_dsi / resp : \n%s', pformat(resp) )
    assert response.status_code == 200
  else :
    return resp


@pytest.mark.get
def test_get_list_dsi( 
  client_access_token,
  as_test = True, 
  page_number=1, 
  results_per_page=100 
  ):
  get_list_dsi( 
    access_token = client_access_token,
    as_test = as_test 
  )



def search_dsi(
  access_token = None,
  dsi_uuid = None,
  q = None,
  version = "last",
  filter_ = None,
  version_n = None,
  page_n = 1,
  per_page = 10,
  sort_by = None,
  sort_order = "asc",
  shuffle_seed = None,
  field_to_return = None,
  fields_to_return = None,
  only_data = False
  ):

  log_.debug("search_dsi / access_token : %s" , access_token )
  
  ### create search params

  query_params = {
    "dsi_uuid": dsi_uuid,
    "q": q,
    "version": "last",
    "filter": filter_,
    "version_n": version_n,
    "page_n": page_n,
    "per_page": per_page,
    "sort_by": sort_by,
    "sort_order": sort_order,
    "shuffle_seed": shuffle_seed,
    "field_to_return": field_to_return,
    "fields_to_return": fields_to_return,
    "only_data": only_data
  }


  ### launch search
  test_result = get_list_dsi(
    access_token = access_token,
    as_test = False,
    page_number = 1, 
    results_per_page = 100, 
    params = query_params
  )

  return test_result

@pytest.mark.get
def test_search_for_dsi(client_access_token):
  
  ### create some DSI 
  identifiers = [ 
    { "title" : "AA", "description" : "aaa BB", "auth_preview" : "private", "auth_modif" : "commons" }, 
    { "title" : "BB", "description" : "bbb CC", "auth_preview" : "opendata", "auth_modif" : "private" }, 
    { "title" : "CC", "description" : "ccc AA BB", "auth_preview" : "private", "auth_modif" : "team" }
  ]
  log_.debug ('=== test_search_for_dsi / identifiers (A) : \n%s', pformat(identifiers) )

  for id in identifiers : 
    payload_ = create_dsi_payload( 
      title_content=id['title'],
      description_content=id['description'],
      auth_preview=id['auth_preview'],
      auth_modif=id['auth_modif']
    )
    log_.debug ('=== test_search_for_dsi / payload_ : \n%s', pformat(payload_) )
    
    test_dsi = create_one_dsi(
      access_token = client_access_token,
      as_test = False,
      payload = payload_,
    )
    log_.debug ('=== test_search_for_dsi / test_dsi : \n%s', pformat(test_dsi) )
    assert test_dsi['data']['is_test_data'] == True
    id['dsi_uuid'] = test_dsi['data']['dsi_uuid']

  log_.debug ('=== test_search_for_dsi / identifiers (B) : \n%s', pformat(identifiers) )

  ### randomly choose a DSI from its identifier
  test_dsi = secure_random.choice( identifiers )

  results = search_dsi(
    access_token = client_access_token,
  )
  log_.debug ('=== test_search_for_dsi / results : \n%s', pformat(results) )



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UTILS DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_random_dsi_uuid( 
  only_test_dsi = False 
  ) : 

  test_dsi_list = get_list_dsi( as_test = False )
  # log_.debug ('=== get_random_dsi_uuid / test_dsi_list : \n%s', pformat(test_dsi_list))

  full_dsi_list = test_dsi_list['data']

  if only_test_dsi : 
    testable_dsi = [ i for i in full_dsi_list if i['is_test_data'] == True ]
    test_dsi = secure_random.choice( testable_dsi )
  else :
    test_dsi = secure_random.choice( full_dsi_list )
  test_dsi_uuid = test_dsi['dsi_uuid']
  log_.debug ('=== get_random_dsi_uuid / test_dsi_uuid : %s', test_dsi_uuid)
  return test_dsi_uuid




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GET ONE DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def get_one_dsi( 
  as_test = True,
  only_test_data = False,
  dsi_uuid = None,
  access_token = None,
  params = None
  ):

  server_api = get_server_api()
  log_.debug ('=== test_get_one_dsi / server_api : %s', server_api)


  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else :
    test_user_access_token = access_token
  
  ### dsi
  if dsi_uuid == None :
    # test_dsi_uuid = '3ffbacf768f1481cb2b8968381490a72'
    # test_dsi_uuid = get_random_dsi_uuid( only_test_dsi = only_test_data ) 
    test_dsi = create_one_dsi ( 
      as_test = False 
    )
    assert test_dsi['data']['is_test_data'] == True
    test_dsi_uuid = test_dsi['data']['dsi_uuid']
  else : 
    test_dsi_uuid = dsi_uuid
  log_.debug ('=== test_get_one_dsi / test_dsi_uuid : %s', test_dsi_uuid)

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/dsi/get_one/{test_dsi_uuid}"
  url = f"{config.API_V1_STR}/dsi/get_one/{test_dsi_uuid}"

  # response = requests.get(
  response = client.get(
    url,
    headers = headers
  )
  resp = response.json()
  log_.debug ('=== test_get_one_dsi / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
  else : 
    return resp


@pytest.mark.get
def test_get_one_dsi(client_access_token):
  log_.debug("test_get_one_dsi / client_access_token : %s" , client_access_token )
  get_one_dsi(
    access_token = client_access_token,
  )









### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UPDATE DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def update_one_dsi( 
  as_test = True, 
  version_n = None,
  update_data = None,
  dsi_uuid = None,
  access_token = None,
  ): 

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else :
    test_user_access_token = access_token
  log_.debug ('=== update_one_dsi / test_user_access_token : %s', test_user_access_token )

  ### create a test DSI
  if dsi_uuid == None :
    test_dsi = create_one_dsi( as_test = False )
    log_.debug ('=== update_one_dsi / test_dsi : \n%s', pformat(test_dsi) )
    assert test_dsi['data']['is_test_data'] == True
    test_dsi_uuid = test_dsi['data']['dsi_uuid'] 
  else : 
    test_dsi_uuid = dsi_uuid
  log_.debug ('=== update_one_dsi / test_dsi_uuid : %s', test_dsi_uuid )

  ### mockup update field
  if update_data == None :
    update_data = {
      "update_data" : {
        "licence" : "my-test-licence",
        "auth_preview" : "private"
      }
    }

  params_update = {
    'version_n' : version_n
  }

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url = f"{server_api}{config.API_V1_STR}/dsi/update/{test_dsi_uuid}"
  url = f"{config.API_V1_STR}/dsi/update/{test_dsi_uuid}"

  ### update doc
  # response = requests.put(
  response = client.put(
    url,
    json = update_data,
    params = params_update,
    headers = headers
  )
  resp = response.json() 
  log_.debug ('=== update_one_dsi / resp : \n%s', pformat(resp) )

  if as_test : 
    assert response.status_code == 200
    for key in update_data['update_data'].keys() :
      assert resp['data'][key] == update_data['update_data'][key]
  else : 
    return resp


@pytest.mark.update
def test_update_one_dsi(client_access_token) :
  update_one_dsi(
    access_token = client_access_token,
  )

@pytest.mark.update
def test_update_one_dsi_with_data(client_access_token) :

  update_data = {
    "update_data" : {
      "auth_modif": "team",
    }
  }

  update_one_dsi(
    access_token = client_access_token,
    update_data = update_data,
  )


### TO DO 
@pytest.mark.update
@pytest.mark.skip(reason='not developped yet')
def test_update_one_dsi_version( ) :

  version_n = 2

  update_data = {
    "update_data" : {
      'description': 'my DSI version description',
    }
  }
  
  update_one_dsi( 
    update_data = update_data,
    version_n = version_n
  )





### - - - - - - - - - - - - - - - - - - - - - - - ### 
### DELETE DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def delete_one_dsi( 
  as_test = True,
  server_api = None,
  dsi_uuid = None, 
  access_token = None,
  full_remove = False,
  ):

  if server_api == None :
    server_api = get_server_api()
    # log_.debug ('=== server_api : %s', server_api)

  if dsi_uuid == None : 
    test_dsi = create_one_dsi( as_test = False ) 
    assert test_dsi['data']['is_test_data'] == True
    dsi_uuid = test_dsi['data']['dsi_uuid']

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
    log_.debug ('=== delete_one_dsi / test_user_access_token : %s', test_user_access_token )
  else :
    test_user_access_token = access_token

  params_delete = {
    'full_remove' : full_remove,
  }
  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  # url =f"{server_api}{config.API_V1_STR}/dsi/remove/{dsi_uuid}"
  url = f"{config.API_V1_STR}/dsi/remove/{dsi_uuid}"

  ### send request
  # response = requests.delete(
  response = client.delete(
    f"{server_api}{config.API_V1_STR}/dsi/remove/{dsi_uuid}",
    params = params_delete,
    headers = headers
  )
  log_.debug ('=== delete_one_dsi / response : \n%s', pformat(response) )

  if as_test : 
    assert response.status_code == 200
  else : 
    # resp = response.json() 
    # log_.debug ('=== delete_one_dsi / resp : \n%s', pformat(resp) )
    # return resp
    return response


@pytest.mark.delete
def test_delete_one_dsi_no_full_remove(client_access_token):
  delete_one_dsi(
    access_token = client_access_token,
    full_remove = False
  )

@pytest.mark.delete
def test_delete_one_dsi_full_remove(client_access_token):
  delete_one_dsi(
    access_token = client_access_token,
    full_remove = True
  )




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### CLEANUP DSI
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def delete_all_dsi( 
  as_test = True, 
  only_test_data = True,
  full_remove = False,
  access_token = None,
  ): 

  server_api = get_server_api()
  # log_.debug ('=== server_api : %s', server_api)

  ### get test user
  if access_token == None :
    test_user_access_token = client_login( as_test = False, only_access_token=True )
  else : 
    test_user_access_token = access_token
  log_.debug ('=== delete_all_dsi / test_user_access_token : %s', test_user_access_token )

  ### get list of DSIs
  test_dsi_list = get_list_dsi( as_test = False )
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
    log_.debug ('=== delete_all_dsi / dsi_uuid : %s', dsi_uuid )
    
    ### send request
    response = delete_one_dsi( 
      as_test = False, 
      server_api = server_api,
      dsi_uuid = dsi_uuid,
      access_token = test_user_access_token,
      full_remove = full_remove
    )
    log_.debug ('=== delete_all_dsi / response : \n%s', pformat(response) )

    assert response.status_code == 200 


@pytest.mark.delete
def test_delete_dsi_no_full_remove(client_access_token): 
  delete_all_dsi( 
    access_token = client_access_token,
    only_test_data = True,
    full_remove = False 
  )

@pytest.mark.delete
def test_delete_dsi_full_remove(client_access_token): 
  delete_all_dsi( 
    access_token = client_access_token,
    only_test_data = True,
    full_remove = True 
  )


### WARNING : RESET TEST !!!
### this test erases ALL DATA in DBs !! 
### comment / uncomment -skip + use at your own risks !!!

@pytest.mark.delete
@pytest.mark.reset
@pytest.mark.skip(reason='DANGEROUS')
def test_delete_ALL_dsi_full_remove(): 
  delete_all_dsi( 
    only_test_data = False,
    full_remove = True 
  )