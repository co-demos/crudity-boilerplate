from log_config import log_, pformat
import inspect 

from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey

from starlette.responses import Response
from starlette.status import *

from models.response import ResponseBase, ResponseDataBase, ResponseBaseNoTotal
from models.dataset_input import DsiBase, Dsi, DsiCreate, DsiUpdate
from models.parameters import *

import crud
from api.utils.security import get_api_key, get_api_key_optional


print()
log_.debug(">>> api/api_v1/endpoints/dataset_inputs.py")


from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)


### test item
test_dsi = {
  'title' : 'test_dsi',
  'dsi_uuid' : 'd7b0cd1b-599a-4f3e-8820-9acc8e1d59e6',
  'owner' : 'system'
}


router = APIRouter()


# @router.get("/list", response_model=List[Dsi])
@router.get("/list")
async def list_dsis(
  resp_: Response,
  dsi_uuid: list = p_dsi_uuid,
  commons: dict = Depends(common_parameters),
  api_key: APIKey = Depends(get_api_key_optional),
  ):
  """GET / get a paginated list of DSIs """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "GET",
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### TO DO / retrieve results given the query 
  res, status = crud.dataset_input.search_dsis(
    query_params = query
  )
  log_.debug( "res : \n%s", pformat(res))

  ### marshal / apply model to data
  if res :
    # data_list =  [ Dsi(**test_dsi) ]
    data_list =  [ Dsi(**res) ]
  else : 
    data_list = []


  time_end = datetime.now()
  stats = {
    'total_items' : len(data_list),
    'queried_at' : str(time_start),  
    'response_at' : str(time_end), 
    'response_delta' : time_end - time_start,  
  }

  if commons['only_data'] == True : 
    log_.debug( "commons['only_data'] == True : %s", commons['only_data'] )
    response = ResponseDataBase(
      status = status,
      data =  data_list,
    )
  else :
    log_.debug( "commons['only_data'] != True : %s", commons['only_data'] )
    response = ResponseBase(
      status = status,
      data =  data_list,
      query = query,
      stats = stats,
    )

  log_.debug( "response : \n%s", pformat( response.dict() ))

  resp_.status_code = status['status_code']
  return response



@router.get("/get_one/{dsi_uuid}")
async def read_dsi( 
  resp_: Response,
  dsi_uuid: uuid.UUID,
  commons: dict = Depends(one_dsi_parameters),
  api_key: APIKey = Depends(get_api_key_optional),
  ):
  """GET / get a specific DSI (without its DSRs) """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "GET",
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  log_.debug( "query : \n%s", pformat(query) )


  ### retrieve results from db and query
  res, status = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = commons,
  )
  log_.debug( "res : \n%s", pformat(res))
  # res = {
  #   'title' : 'test_dsi',
  #   'dsi_uuid' : dsi_uuid ,
  #   'owner' : 'system'
  # }

  ### marshal / apply model to data
  if res : 
    data =  Dsi(**res)
  else : 
    data = None


  if commons['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = data,
    )
  else : 
    time_end = datetime.now()
    stats = {
      'total_items' : len([data]),
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBase(
      status = status,
      query = query,
      data =  data,
      stats = stats,
    )

  resp_.status_code = status['status_code']
  return response



@router.post("/create")
async def create_dsi(
  *,
  resp_: Response,
  dsi_in: DsiCreate,
  resp_p: dict = Depends(resp_parameters),
  api_key: APIKey = Depends(get_api_key),
  ):
  """ post a new DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / %s", inspect.stack()[0][3] )
  log_.debug( "dsi_in : \n%s", pformat( dsi_in.dict() ) )
  log_.debug( "resp_p : \n%s", pformat( resp_p ) )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "POST",
    **resp_p,
  }

  ### build / marshall a dsi from models
  dsi_client = DsiBase( **dsi_in.dict() )
  dsi_client_dict = dsi_client.dict()

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsi_uuid = crud.utils.generate_new_id()
  dsi_client_dict['dsi_uuid'] = dsi_uuid
  dsi_db = Dsi(**dsi_client_dict)
  log_.debug( "dsi_db : \n%s", pformat( dsi_db.dict() ) )

  ### add in DBs
  res, status = crud.dataset_input.create_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    body = dsi_db.dict()
  )
  log_.debug( "res : \n%s", pformat(res))

  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = dsi_db,
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
      data =  dsi_db,
      stats = stats,
    )

  resp_.status_code = status['status_code']
  return response



@router.put("/update/{dsi_uuid}")
async def update_dsi(
  *,
  resp_: Response,
  dsi_uuid: uuid.UUID,
  body: dict,
  resp_p: dict = Depends(resp_parameters),
  api_key: APIKey = Depends(get_api_key),
  ):
  """ update a specific DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "PUT / %s", inspect.stack()[0][3] )
  log_.debug( "body : \n%s", pformat(body) )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "PUT",
    "dsi_uuid": dsi_uuid,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### update in DBs
  res, status = crud.dataset_input.update_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    body = body
  )
  log_.debug( "res : \n%s", pformat(res))


  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = body,
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
      data =  body,
      stats = stats,
    )

  resp_.status_code = status['status_code']
  return response



@router.delete("/remove/{dsi_uuid}")
async def delete_dsi(
  resp_: Response,
  dsi_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  remove_p: dict = Depends(delete_parameters),
  api_key: APIKey = Depends(get_api_key),
  ):
  """ delete a specific DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "DELETE / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "DELETE",
    "dsi_uuid": dsi_uuid,
    **resp_p,
    **remove_p,
  }
  log_.debug( "query : \n%s", pformat(query) )


  ### 1 - delete corresponding DSI 
  res, status = crud.dataset_input.remove_dsi(
    dsi_uuid = dsi_uuid,
  )
  log_.debug( "res : \n%s", pformat(res))


  res = {
    "dsi_deleted" : dsi_uuid
  }

  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = res,
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
    )

  resp_.status_code = status['status_code']
  return response
