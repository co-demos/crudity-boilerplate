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

from models.response import ResponseBase, ResponseDataBase, ResponseBaseResp
from models.dataset_raw import Dsr, DsrCreate, DsrUpdate, DsrData, DsrUpdateData
from models.parameters import *

import crud
from api.utils.security import get_api_key, get_api_key_optional, get_user_infos, need_user_infos


print()
log_.debug(">>> api/api_v1/endpoints/dataset_inputs.py")


router = APIRouter()



@router.get("/dataset/{dsi_uuid}")
async def read_dsi_items(
  resp_: Response,

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to retrieve DSRs from"),
  # dsi_uuid: p_dsi_uuid,
  # dsi_uuid: uuid.UUID,

  dsr_uuid: list = p_dsr_uuid,
  commons: dict = Depends(search_dsrs_parameters),
  include_src: bool = p_include_src,

  # api_key: APIKey = Depends(get_api_key_optional),
  user: dict = Depends(get_user_infos),
  ):
  """ get paginated DSRs from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  msg = ""
  doc_version = {
    'version_n' : None,
    'version_s' : None
  }

  query = { 
    "method" : "GET",
    'dsr_uuid': dsr_uuid,
    'include_src' : include_src,
    **commons,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### 1 - get corresponding DSI from dsi_uuid
  res_dsi, status_dsi = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  doc_version['version_n'] = res_dsi['_version']
  doc_version['version_s'] = commons['version']
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### 2 - get corresponding DSRs from dsi_uuid as index_name
  if status_dsi['status_code'] == 200 :
    res_dsrs, status_dsr = crud.dataset_raw.search_dsrs(
      dsi_uuid = dsi_uuid,
      query_params = query,
    )
    log_.debug( "res_dsrs : \n%s", pformat(res_dsrs))
    msg = 'DSI found but not DSRs yet...'
  else : 
    res_dsrs = None


  if status_dsr['status_code'] == 200 : 
    data_list = res_dsrs
    msg = 'here comes the list of DSRs corresponding to this DSI'
  else :
    data_list = []



  # response = {"dsi_id": dsi_uuid}

  if commons['only_data'] == True : 
    log_.debug( "commons['only_data'] == True : %s", commons['only_data'] )
    response = ResponseDataBase(
      status = status_dsr,
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
      'total_items' : status_dsr.get('total', 0),
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBase(
      status = status_dsr,
      data =  data_list,
      query = query,
      stats = stats,
      doc_version = doc_version,
      msg = msg
    )

  log_.debug( "response : \n%s", pformat( response.dict() ))

  resp_.status_code = status_dsr['status_code']
  return response



@router.get("/dataset/{dsi_uuid}/dsr/get_one/{dsr_uuid}")
async def read_dsr_item(
  resp_: Response,

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to use"),
  dsr_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSR item to retrieve"),
  # dsi_uuid: str,
  # dsr_uuid: str,
  # dsi_uuid: uuid.UUID,
  # dsr_uuid: uuid.UUID,

  resp_p: dict = Depends(one_dsr_parameters),
  # api_key: APIKey = Depends(get_api_key_optional),
  user: dict = Depends(get_user_infos),
  ):
  """ get one DSR from a DSI """
 
  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "GET",
    'dsi_uuid': dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  ### 1 - get corresponding DSI from dsi_uuid
  msg = ""
  doc_version = {
    'version_n' : None,
    'version_s' : None
  }
  res_dsi, status_dsi = crud.dataset_input.view_dsi(
    dsi_uuid = dsi_uuid,
    query_params = query,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### 2 - get corresponding DSR from dsi_uuid as index_name and dsr_uuid
  res, status = crud.dataset_raw.view_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
  )
  log_.debug( "res : \n%s", pformat(res))


  ### marshal / apply model to data
  if res : 
    # data =  Dsi(**res)
    data = Dsr( **res['_source'] )
    doc_version['version_n'] = res['_version']
    doc_version['version_s'] = resp_p['version']
  else : 
    data = None


  time_end = datetime.now()
  # response =  {"dsr_uuid": dsr_uuid}
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

  resp_.status_code = status_dsi['status_code']
  return response



### - - - - - - - - - - - - - - - - - - - - - ### 
### NEED AUTH
### - - - - - - - - - - - - - - - - - - - - - ### 

@router.post("/dataset/{dsi_uuid}/dsr/create")
async def create_dsr_item(
  *,
  resp_: Response,
  item_data: DsrData,

  resp_p: dict = Depends(resp_parameters),

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to post on"),
  # dsi_uuid: uuid.UUID,
  # dsi_uuid: str,
  
  # api_key: APIKey = Depends(get_api_key),
  user: dict = Depends(need_user_infos),
  ):
  """ post one DSR into a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "POST",
    'dsi_uuid': dsi_uuid,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  log_.debug( "item_data : \n%s", pformat( item_data.dict() ) )
  item_data_dict = item_data.dict()
  item_data_ = item_data_dict


  msg = '' 

  ### 1 - post corresponding DSR from dsi_uuid as index_name and dsr_uuid as id

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsr_uuid = crud.utils.generate_new_id()

  ### add infos
  item_data_['dsi_uuid'] = dsi_uuid
  item_data_['dsr_uuid'] = dsr_uuid
  item_data_['created_at'] = datetime.now()
  item_data_['created_by'] = user['infos']['email']
  item_data_['owner'] = user['infos']['email']
  log_.debug( "item_data_ (A): \n%s", pformat( item_data_ ) )

  ### add in DBs
  res, status = crud.dataset_raw.create_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
    body = item_data_
  )
  log_.debug( "res : \n%s", pformat(res))
  log_.debug( "status : \n%s", pformat(status))
  log_.debug( "item_data_ (B): \n%s", pformat( item_data_ ) )

  try : 
    del item_data_["_id"]
  except : 
    pass
  log_.debug( "item_data_ (C): \n%s", pformat( item_data_ ) )

  ### response formatting
  if status['status_code'] == 200 : 
    msg = f"the DSR doc has been created for DSI dataset with dsi_uuid <{dsi_uuid}> "
  else : 
    msg = f"there has been an error while creating DSR doc with dsi_uuid <{dsi_uuid}>"

  if resp_p['only_data'] == True : 
    response = ResponseDataBase(
      status = status,
      data = item_data_,
      msg = msg
    )
  else : 
    time_end = datetime.now()
    stats = {
      'queried_at' : str(time_start),  
      'response_at' : str(time_end), 
      'response_delta' : time_end - time_start,  
    }
    response = ResponseBaseResp(
      status = status,
      query = query,
      data =  item_data_,
      resp = res,
      stats = stats,
      msg = msg,
    )


  resp_.status_code = status['status_code']
  return response



@router.put("/dataset/{dsi_uuid}/dsr/update/{dsr_uuid}")
async def update_dsr_item(
  *,
  resp_: Response,

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to use"),
  dsr_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSR item to update"),
  # dsi_uuid: str,
  # dsr_uuid: str,
  # dsi_uuid: uuid.UUID,
  # dsr_uuid: uuid.UUID,

  update_p: dict = Depends(update_parameters),
  resp_p: dict = Depends(resp_parameters),
  item_data: DsrUpdateData,

  # api_key: APIKey = Depends(get_api_key),
  user: dict = Depends(need_user_infos),
  ):
  """ update one DSR from a DSI """

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "PUT / %s", inspect.stack()[0][3] )
  log_.debug( "item_data : \n%s", pformat(item_data) )
  time_start = datetime.now()

  # log_.debug( "api_key : %s", api_key )
  log_.debug( "user : \n%s", pformat(user) )

  query = {
    "method" : "PUT",
    'dsi_uuid': dsi_uuid,
    'dsr_uuid': dsr_uuid,
    **update_p,
    **resp_p,
  }
  log_.debug( "query : \n%s", pformat(query) )

  log_.debug( "item_data : \n%s", pformat( item_data.dict() ) )
  item_data_dict = item_data.dict()
  item_data_ = item_data_dict

  msg = '' 

  ### 1 - update corresponding DSR from dsi_uuid as index_name and dsr_uuid as id

  ### update in DBs
  res, status = crud.dataset_raw.update_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
    body = item_data_
  )
  log_.debug( "res : \n%s", pformat(res))



  if status['status_code'] == 200 : 
    msg = f"the DSR doc with dsr_uuid <{dsr_uuid}> has been updated"
  else : 
    msg = f"there has been an error while updating DSR doc with dsr_uuid <{dsr_uuid}>"

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
    response = ResponseBaseResp(
      status = status,
      query = query,
      data =  item_data_,
      response =  res,
      stats = stats,
      msg = msg
    )



  resp_.status_code = status['status_code']
  return response



@router.delete("/dataset/{dsi_uuid}/dsr/remove/{dsr_uuid}")
async def delete_dsr_item(
  resp_: Response,

  dsi_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSI item to delete from"),
  dsr_uuid: str = Path(..., title="item UUID", description="`str` : UUID of the DSR item to delete"),
  # dsi_uuid: str,
  # dsr_uuid: str,
  # dsi_uuid: uuid.UUID,
  # dsr_uuid: uuid.UUID,

  resp_p: dict = Depends(resp_parameters),
  remove_p: dict = Depends(delete_parameters),
  version_p: dict = Depends(version_parameters),
  # api_key: APIKey = Depends(get_api_key),
  user: dict = Depends(need_user_infos),
  ):
  """ delete one DSR from a DSI """

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
    'dsr_uuid': dsr_uuid,
    **resp_p,
    **remove_p,
    **version_p
  }
  log_.debug( "query : \n%s", pformat(query) )

  msg = '' 

  ### delete DSR doc with dsi_uuid as index_name and dsr_uuid as id
  res, status = crud.dataset_raw.remove_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query,
  )
  log_.debug( "res : \n%s", pformat(res))


  if status == 200 : 
    msg = f"the DSR doc with dsi_uuid <{dsr_uuid}> has been deleted"
  else : 
    msg = f"there has been an error while deleting DSR doc with dsi_uuid <{dsr_uuid}>"

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
    response = ResponseBaseResp(
      status = status,
      query = query,
      data =  res,
      response = res,
      stats = stats,
      msg = msg
    )

  resp_.status_code = status['status_code']
  return response