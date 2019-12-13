from log_config import log_, pformat

from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException

from models.response import ResponseBase, ResponseDataBase
from models.dataset_raw import Dsr, DsrCreate, DsrUpdate, DsrData
from models.parameters import *

import crud

print()
log_.debug(">>> api/api_v1/endpoints/dataset_inputs.py")


router = APIRouter()


@router.get("/dataset/{dsi_uuid}")
async def read_dsi_items(
  dsi_uuid: uuid.UUID,
  dsr_uuid: list = dsr_uuid,
  commons: dict = Depends(common_parameters)
  ):
  """ get paginated DSRs from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / new request / read_dsi_items " )
  time_start = datetime.now()

  query = { 
    "method" : "GET",
    'dsr_uuid': dsr_uuid,
    **commons
  }
  log_.debug( "query : %s", query )

  ### 1 - get corresponding DSI from dsi_uuid
  res_dsi = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### 2 - get corresponding DSRs from dsi_uuid as index_name
  res_dsrs = crud.dataset_raw.search_dsrs(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  log_.debug( "res_dsrs : \n%s", pformat(res_dsrs))



  time_end = datetime.now()
  response = {"dsi_id": dsi_uuid}
  return response




@router.get("/dataset/{dsi_uuid}/dsr/get_one/{dsr_uuid}")
async def read_dsr_item(
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  ):
  """ get one DSR from a DSI """
 
  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / new request / read_dsr_item " )
  time_start = datetime.now()

  query = {
    "method" : "GET",
    'dsi_uuid': dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
  }
  log_.debug( "query : %s", query )

  ### 1 - get corresponding DSI from dsi_uuid
  res_dsi = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### 2 - get corresponding DSR from dsi_uuid as index_name and dsr_uuid
  res_dsr = crud.dataset_raw.view_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
  )
  log_.debug( "res_dsr : \n%s", pformat(res_dsr))



  time_end = datetime.now()
  response =  {"dsr_uuid": dsr_uuid}
  return response



@router.post("/dataset/{dsi_uuid}/dsr/create")
async def create_dsr_item(
  *,
  dsi_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  item_data: DsrData,
  ):
  """ post one DSR into a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / new request / create_dsr_item " )
  time_start = datetime.now()

  query = {
    "method" : "POST",
    'dsi_uuid': dsi_uuid,
    **resp_p,
  }
  log_.debug( "query : %s", query )

  ### 1 - post corresponding DSR from dsi_uuid as index_name and dsr_uuid as id

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsr_uuid = crud.utils.generate_new_id()
  
  ### add in DBs
  res = crud.dataset_raw.create_dsr(
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
  return response


@router.put("/dataset/{dsi_uuid}/dsr/update/{dsr_uuid}")
async def update_dsr_item(
  *,
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  item_data: DsrData,
  ):
  """ update one DSR from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "PUT / new request / update_dsr_item " )
  log_.debug( "item_data : \n%s", pformat(item_data) )
  time_start = datetime.now()

  query = {
    "method" : "PUT",
    'dsi_uuid': dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
  }
  log_.debug( "query : %s", query )

  ### 1 - update corresponding DSR from dsi_uuid as index_name and dsr_uuid as id

  ### update in DBs
  res = crud.dataset_raw.update_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
    body = item_data
  )
  log_.debug( "res : \n%s", pformat(res))


  time_end = datetime.now()
  response =  {"dsr_uuid": dsr_uuid}
  return response


@router.delete("/dataset/{dsi_uuid}/dsr/remove/{dsr_uuid}")
async def delete_dsr_item(
  dsi_uuid: uuid.UUID,
  dsr_uuid: uuid.UUID,
  resp_p: dict = Depends(resp_parameters),
  remove_p: dict = Depends(delete_parameters),
  ):
  """ delete one DSR from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "DELETE / new request / delete_dsr " )
  time_start = datetime.now()

  query = {
    "method" : "DELETE",
    "dsi_uuid": dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
    **remove_p,
  }
  log_.debug( "query : %s", query )


  ### 1 - delete corresponding DSR from dsi_uuid as index_name and dsr_uuid as id
  res = crud.dataset_input.remove_dsi(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
  )
  log_.debug( "res : \n%s", pformat(res))


  time_end = datetime.now()
  response =  {"dsr_uuid": dsr_uuid}  
  return response