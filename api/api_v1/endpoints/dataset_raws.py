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

from models.response import ResponseBase, ResponseDataBase
from models.dataset_raw import Dsr, DsrCreate, DsrUpdate, DsrData
from models.parameters import *

import crud
from api.utils.security import get_api_key, get_api_key_optional


print()
log_.debug(">>> api/api_v1/endpoints/dataset_inputs.py")


router = APIRouter()


@router.get("/dataset/{dsi_uuid}")
async def read_dsi_items(
  resp_: Response,
  dsi_uuid: uuid.UUID,
  dsr_uuid: list = p_dsr_uuid,
  commons: dict = Depends(search_dsrs_parameters),
  api_key: APIKey = Depends(get_api_key_optional),
  ):
  """ get paginated DSRs from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = { 
    "method" : "GET",
    'dsr_uuid': dsr_uuid,
    **commons
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### 1 - get corresponding DSI from dsi_uuid
  res_dsi, status_dsi = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### 2 - get corresponding DSRs from dsi_uuid as index_name
  if status_dsi['status_code'] == 200 :
    res_dsrs, status_dsr = crud.dataset_raw.search_dsrs(
      dsi_uuid = dsi_uuid,
      query_params = query,
    )
    log_.debug( "res_dsrs : \n%s", pformat(res_dsrs))
  else : 
    res_dsrs = None

  time_end = datetime.now()
  response = {"dsi_id": dsi_uuid}




  resp_.status_code = status_dsi['status_code']
  return response




@router.get("/dataset/{dsi_uuid}/dsr/get_one/{dsr_uuid}")
async def read_dsr_item(
  resp_: Response,
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  resp_p: dict = Depends(one_dsr_parameters),
  api_key: APIKey = Depends(get_api_key_optional),
  ):
  """ get one DSR from a DSI """
 
  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "GET",
    'dsi_uuid': dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### 1 - get corresponding DSI from dsi_uuid
  res_dsi, status_dsi = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### 2 - get corresponding DSR from dsi_uuid as index_name and dsr_uuid
  res_dsr, status_dsr = crud.dataset_raw.view_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
  )
  log_.debug( "res_dsr : \n%s", pformat(res_dsr))



  time_end = datetime.now()
  response =  {"dsr_uuid": dsr_uuid}

  resp_.status_code = status_dsi['status_code']
  return response



@router.post("/dataset/{dsi_uuid}/dsr/create")
async def create_dsr_item(
  *,
  resp_: Response,
  dsi_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  item_data: DsrData,
  api_key: APIKey = Depends(get_api_key),
  ):
  """ post one DSR into a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "POST",
    'dsi_uuid': dsi_uuid,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### 1 - post corresponding DSR from dsi_uuid as index_name and dsr_uuid as id

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsr_uuid = crud.utils.generate_new_id()
  
  ### add in DBs
  res, status = crud.dataset_raw.create_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
    body = item_data
  )



  time_end = datetime.now()
  response =  {
    "dsr_uuid": dsr_uuid,
    "item_data": item_data
  }

  resp_.status_code = status['status_code']
  return response


@router.put("/dataset/{dsi_uuid}/dsr/update/{dsr_uuid}")
async def update_dsr_item(
  *,
  resp_: Response,
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  item_data: DsrData,
  api_key: APIKey = Depends(get_api_key),
  ):
  """ update one DSR from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "PUT / %s", inspect.stack()[0][3] )
  log_.debug( "item_data : \n%s", pformat(item_data) )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "PUT",
    'dsi_uuid': dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### 1 - update corresponding DSR from dsi_uuid as index_name and dsr_uuid as id

  ### update in DBs
  res, status = crud.dataset_raw.update_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
    body = item_data
  )
  log_.debug( "res : \n%s", pformat(res))


  time_end = datetime.now()
  response =  {"dsr_uuid": dsr_uuid}

  resp_.status_code = status['status_code']
  return response


@router.delete("/dataset/{dsi_uuid}/dsr/remove/{dsr_uuid}")
async def delete_dsr_item(
  resp_: Response,
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  remove_p: dict = Depends(delete_parameters),
  api_key: APIKey = Depends(get_api_key),
  ):
  """ delete one DSR from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "DELETE / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "api_key : %s", api_key )

  query = {
    "method" : "DELETE",
    "dsi_uuid": dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
    **remove_p,
  }
  log_.debug( "query : \n%s", pformat(query) )


  ### 1 - delete corresponding DSR from dsi_uuid as index_name and dsr_uuid as id
  res, status = crud.dataset_input.remove_dsi(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
  )
  log_.debug( "res : \n%s", pformat(res))


  time_end = datetime.now()
  response =  {"dsr_uuid": dsr_uuid}

  resp_.status_code = status['status_code']
  return response