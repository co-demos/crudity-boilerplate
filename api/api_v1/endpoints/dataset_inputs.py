from log_config import log_, pformat
import inspect 

from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security.api_key import APIKey

from starlette.responses import Response
from starlette.status import *

from models.response import ResponseBase, ResponseDataBase, ResponseBaseNoTotal
from models.dataset_input import DsiBase, Dsi, DsiCreate, DsiUpdate, DsiUpdateIn, DsiEs, DsiESList
from models.parameters import *

import crud
from core import config
from api.utils.security import get_api_key, get_api_key_optional, get_user_infos, need_user_infos


print()
log_.debug(">>> api/api_v1/endpoints/dataset_inputs.py")


from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)

router = APIRouter()

auth_active = config.AUTH_MODE != 'no_auth' 


# @router.get("/list", response_model=List[Dsi])
@router.get("/list")
async def list_of_dsi_items(
  resp_: Response,
  dsi_uuid: list = p_dsi_uuid,
  commons: dict = Depends(common_parameters),
  # api_key: APIKey = Depends(get_api_key_optional),
  user: dict = Depends(get_user_infos),
  ):
  """GET / get a paginated list of DSIs """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "GET",
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  log_.debug( "query : \n%s", pformat(query) )

  msg = ''
  doc_version = {
    'version_n' : None,
    'version_s' : None
  }

  ### TO DO / retrieve results given the query 
  res, status = crud.dataset_input.search_dsis(
    query_params = query,
    user = user,
  )
  # log_.debug( "res : \n%s", pformat(res))

  ### marshal / apply model to data
  if res :
    # data_list =  [ Dsi(**test_dsi) ]
    # data_list =  [ Dsi(**res) ]
    # data_list = DsiESList( dsis=res )
    # data_list = data_list.dsis

    # doc_version['version_n'] = res['_version']
    doc_version['version_s'] = commons['version']

    data_list =  [ 
      Dsi( **r['_source'] ) for r in res 
    ]
    # log_.debug( "data_list : \n%s", pformat( data_list ))
    # data_list = [ DsiEs(**item) for item in res ]
    # log_.debug( "data_list : \n%s", pformat( data_list ))
    msg = 'here comes your list of available DSIs'
  else : 
    data_list = []
    msg = 'no DSI yet in database'



  if commons['only_data'] == True : 
    log_.debug( "commons['only_data'] == True : %s", commons['only_data'] )
    response = ResponseDataBase(
      status = status,
      data =  data_list,
      doc_version = doc_version,
      msg = msg
    )
  else :
    log_.debug( "commons['only_data'] != True : %s", commons['only_data'] )
    time_end = datetime.now()
    stats = {
      'page_n' : query['page_n'],
      'per_page' : query['per_page'].value,
      # 'total_items' : len(data_list),
      'total_items' : status.get('total', 0),
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBase(
      status = status,
      data =  data_list,
      query = query,
      stats = stats,
      doc_version = doc_version,
      msg = msg
    )

  # log_.debug( "response : \n%s", pformat( response.dict() ))

  resp_.status_code = status['status_code']
  return response



@router.get("/get_one/{dsi_uuid}")
async def read_dsi_item( 

  resp_: Response,

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the item DSI to retrieve"),
  # dsi_uuid: str,
  # dsi_uuid: uuid.UUID,

  commons: dict = Depends(one_dsi_parameters),
  # api_key: APIKey = Depends(get_api_key_optional),
  user: dict = Depends(get_user_infos),
  ):
  """GET / get a specific DSI (without its DSRs) """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "GET",
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  log_.debug( "query : \n%s", pformat(query) )


  ### retrieve results from db and query
  msg = ''
  doc_version = {
    'version_n' : None,
    'version_s' : None
  }
  res, status = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = commons,
    user = user,
  )
  # log_.debug( "res : \n%s", pformat(res))


  ### marshal / apply model to data
  if res : 
    data = Dsi( **res['_source'] )
    doc_version['version_n'] = res['_version']
    doc_version['version_s'] = commons['version']
    msg = 'here comes your dsi'
  else : 
    data = None
    msg = 'no such dsi in database'


  if commons['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = data,
      doc_version = doc_version,
      msg = msg
    )
  else : 
    time_end = datetime.now()
    stats = {
      # 'total_items' : len([data]),
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBase(
      status = status,
      query = query,
      data =  data,
      stats = stats,
      doc_version = doc_version,
      msg = msg
    )

  resp_.status_code = status['status_code']
  return response



### - - - - - - - - - - - - - - - - - - - - - ### 
### NEED AUTH
### - - - - - - - - - - - - - - - - - - - - - ### 

@router.post("/create")
async def create_dsi_item(
  *,
  resp_: Response,
  dsi_in: DsiCreate,
  resp_p: dict = Depends(resp_parameters),
  # api_key: APIKey = Depends(get_api_key),
  user: dict = Depends(need_user_infos),
  ):
  """ post a new DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / %s", inspect.stack()[0][3] )
  log_.debug( "dsi_in : \n%s", pformat( dsi_in.dict() ) )
  log_.debug( "resp_p : \n%s", pformat( resp_p ) )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "POST",
    **resp_p,
  }

  msg = '' 
  doc_version = {
    'version_n' : None,
    'version_s' : None
  }

  ### build / marshall a dsi from models
  dsi_client = DsiBase( **dsi_in.dict() )
  dsi_client_dict = dsi_client.dict()
  log_.debug( "dsi_client_dict : \n%s", pformat( dsi_client_dict ) )

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsi_uuid = crud.utils.generate_new_id()
  log_.debug( "dsi_uuid : %s", dsi_uuid )
  dsi_client_dict['dsi_uuid'] = dsi_uuid

  ### add 
  dsi_client_dict['created_at'] = datetime.now()
  dsi_client_dict['created_by'] = user['infos']['email']
  dsi_client_dict['owner'] = user['infos']['email']


  ### format as DSI for DB
  dsi_db = Dsi( **dsi_client_dict )
  dsi_db_ = dsi_db.dict()
  log_.debug( "dsi_db_ : \n%s", pformat( dsi_db_ ) )

  ### add in DBs
  res, status = crud.dataset_input.create_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    body = dsi_db_
  )
  log_.debug( "res : \n%s", pformat(res))
  
  ### populate response fields from res
  if res : 
    data = Dsi( **dsi_db_ ) 
    doc_version['version_n'] = res['_version']
    doc_version['version_s'] = 'last'
  else :
    data = None

  ### status from res
  if status['status_code'] == 200 : 
    msg = 'your DSI document has been created'
  else : 
    msg = "there has been an error while creating your DSI document"

  ### response formatting
  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = data,
      msg = msg
    )
  else : 
    time_end = datetime.now()
    stats = {
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBaseNoTotal(
      status = status,
      query = query,
      data =  data,
      stats = stats,
      msg = msg
    )

  log_.debug( "response : \n%s", pformat( response.dict() ))

  resp_.status_code = status['status_code']
  return response



@router.put("/update/{dsi_uuid}")
async def update_dsi_item(
  *,
  resp_: Response,

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to update"),
  # dsi_uuid: str,
  # dsi_uuid: uuid.UUID,

  # body: DsiUpdateIn,
  body: DsiUpdate,
  
  resp_p: dict = Depends(resp_parameters),
  # api_key: APIKey = Depends(get_api_key),
  user: dict = Depends(need_user_infos),
  ):
  """ update a specific DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "PUT / %s", inspect.stack()[0][3] )
  log_.debug( "body : \n%s", pformat(body) )
  time_start = datetime.now()

  log_.debug( "user : \n%s", pformat(user) )


  query = {
    "method" : "PUT",
    "dsi_uuid": dsi_uuid,
    # **update_p,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  msg = '' 
  doc_version = {
    'version_n' : None,
    'version_s' : None
  }

  ### refilter body
  body_filtered = DsiUpdateIn(
    **body.update_data,
    modified_at = datetime.now(),
    modified_by = user['infos']['email'],
  )
  body_filtered_dict = body_filtered.dict()
  # log_.debug( "body_filtered_dict : \n%s", pformat( body_filtered_dict ) )
  
  allowed_keys = [ 'modified_at', 'modified_by', *body.update_data.keys() ]
  # log_.debug( "allowed_keys : \n%s", pformat(allowed_keys) )
  
  ### filter out keys from body
  body_filtered_dict_ = { k : body_filtered_dict[k] for k in body_filtered_dict.keys() if k in allowed_keys }
  log_.debug( "body_filtered_dict_ : \n%s", pformat(body_filtered_dict_) )



  ### update in DBs
  res, status = crud.dataset_input.update_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    body = body_filtered_dict_,
    user = user,
  )
  log_.debug( "res : \n%s", pformat(res))


  ### data from res
  if res : 
    data = res['_source']
    doc_version['version_n'] = res['_version']
    doc_version['version_s'] = 'last'
  else :
    data = None

  ### status from res
  if status['status_code'] == 200 : 
    msg = f"the DSI doc with dsi_uuid <{dsi_uuid}> has been updated"
  else : 
    msg = f"there has been an error while updating DSI doc with dsi_uuid <{dsi_uuid}>"



  ### trim response
  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      # data = body,
      data = data,
      doc_version = doc_version,
      msg = msg 
    )
  else : 
    time_end = datetime.now()
    stats = {
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBaseNoTotal(
      status = status,
      query = query,
      # data =  body,
      data = data,
      doc_version = doc_version,
      stats = stats,
      msg = msg 
    )


  ### return response
  resp_.status_code = status['status_code']
  return response



@router.delete("/remove/{dsi_uuid}")
async def delete_dsi_item(
  resp_: Response,

  # dsi_uuid: str,
  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to delete"),
  # dsi_uuid: uuid.UUID,

  resp_p: dict = Depends(resp_parameters),
  remove_p: dict = Depends(delete_parameters),
  version_p: dict = Depends(version_parameters),
  # api_key: APIKey = Depends(get_api_key),
  user: dict = Depends(need_user_infos),
  ):
  """ delete a specific DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "DELETE / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "DELETE",
    "dsi_uuid": dsi_uuid,
    **resp_p,
    **remove_p,
    **version_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  msg = '' 

  ### 1 - delete corresponding DSI 
  res, status = crud.dataset_input.remove_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    user = user,
  )
  log_.debug( "res : \n%s", pformat(res))
  log_.debug( "status : \n%s", pformat(status))

  ### message
  if status['status_code'] == 200 : 
    if query['full_remove'] : 
      msg = f"the DSI doc with dsi_uuid <{dsi_uuid}> has been fully deleted"
    else : 
      msg = f"the DSI doc with dsi_uuid <{dsi_uuid}> has been tagged as deleted"
  else : 
    msg = f"there has been an error while deleting DSI doc with dsi_uuid <{dsi_uuid}>"

  ### trim response
  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = res,
      msg = msg
    )
  else : 
    time_end = datetime.now()
    stats = {
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBase(
      status = status,
      query = query,
      data =  res,
      stats = stats,
      msg = msg
    )

  ### return 
  resp_.status_code = status['status_code']
  return response
