from log_config import log_, pformat

from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException

from models.response import ResponseBase, ResponseDataBase, ResponseBaseNoTotal
from models.dataset_input import DsiBase, Dsi, DsiCreate, DsiUpdate
from models.parameters import *

import crud

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
  dsi_uuid: list = dsi_uuid,
  commons: dict = Depends(common_parameters)
  ):
  """GET / get a paginated list of DSIs """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "new request / list_dsis " )
  time_start = datetime.now()

  query = {
    "method" : "GET",
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  log_.debug( "query : %s", query )

  ### TO DO / retrieve results given the query 
  res = crud.dataset_input.search_dsis(
    query_params = query
  )
  log_.debug( "res : \n%s", pformat(res))

  ### marshal / apply model to data
  data_list =  [ Dsi(**test_dsi) ]


  time_end = datetime.now()
  stats = {
    'total_items' : len(data_list),
    'queried_at' : str(time_start),  
    'response_at' : str(time_end), 
    'response_delta' : time_end - time_start,  
  }

  if only_data == True : 
    response = ResponseDataBase(
      data =  data_list,
    )
  else :
    response = ResponseBase(
      query = query,
      data =  data_list,
      stats = stats,
    )

  return response



@router.get("/get_one/{dsi_uuid}")
async def read_dsi( 
  dsi_uuid: uuid.UUID,
  commons: dict = Depends(one_dsi_parameters)
  ):
  """GET / get a specific DSI (without its DSRs) """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "new request / read_dsi " )
  time_start = datetime.now()

  query = {
    "method" : "GET",
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  log_.debug( "query : %s", query )


  ### retrieve results from db and query
  res = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = commons,
  )
  log_.debug( "res : \n%s", pformat(res))
  res = {
    'title' : 'test_dsi',
    'dsi_uuid' : dsi_uuid ,
    'owner' : 'system'
  }

  ### marshal / apply model to data
  data =  Dsi(**res)


  if only_data == True : 
    response = ResponseDataBase(
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
      query = query,
      data =  data,
      stats = stats,
    )

  return response



@router.post("/create")
async def create_dsi(
  *,
  dsi_in: DsiCreate,
  resp_p: dict = Depends(resp_parameters),
  ):
  """ post a new DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / new request / create_dsi " )
  log_.debug( "dsi_in : \n%s", pformat(dsi_in) )
  log_.debug( "resp_p : \n%s", pformat(resp_p) )
  time_start = datetime.now()

  query = {
    "method" : "POST",
    **resp_p,
  }


  dsi_client = DsiBase( **dsi_in.dict() )
  dsi_client_dict = dsi_client.dict()

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsi_uuid = crud.utils.generate_new_id()
  dsi_client_dict['dsi_uuid'] = dsi_uuid
  dsi_db = Dsi(**dsi_client_dict)

  ### add in DBs
  res = crud.dataset_input.create_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    body = dsi_db
  )
  log_.debug( "res : \n%s", pformat(res))

  if only_data == True : 
    response = ResponseDataBase(
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
      query = query,
      data =  dsi_db,
      stats = stats,
    )

  return response



@router.put("/update/{dsi_uuid}")
async def update_dsi(
  *,
  dsi_uuid: uuid.UUID,
  body: dict,
  resp_p: dict = Depends(resp_parameters),
  ):
  """ update a specific DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "PUT / new request / update_dsi " )
  log_.debug( "body : \n%s", pformat(body) )
  time_start = datetime.now()

  query = {
    "method" : "PUT",
    "dsi_uuid": dsi_uuid,
    **resp_p,
  }
  log_.debug( "query : %s", query )

  ### update in DBs
  res = crud.dataset_input.update_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
    body = body
  )
  log_.debug( "res : \n%s", pformat(res))


  if only_data == True : 
    response = ResponseDataBase(
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
      query = query,
      data =  body,
      stats = stats,
    )

  return response



@router.delete("/remove/{dsi_uuid}")
async def delete_dsi(
  dsi_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  remove_p: dict = Depends(delete_parameters),
  ):
  """ delete a specific DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "DELETE / new request / delete_dsi " )
  time_start = datetime.now()

  query = {
    "method" : "DELETE",
    "dsi_uuid": dsi_uuid,
    **resp_p,
    **remove_p,
  }
  log_.debug( "query : %s", query )


  ### 1 - delete corresponding DSI 
  res = crud.dataset_input.remove_dsi(
    dsi_uuid = dsi_uuid,
  )
  log_.debug( "res : \n%s", pformat(res))


  res = {
    "dsi_deleted" : dsi_uuid
  }

  if only_data == True : 
    response = ResponseDataBase(
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
      query = query,
      data =  res,
      stats = stats,
    )

  return response
