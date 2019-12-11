from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException

from models.response import ResponseBase, ResponseDataBase
from models.dataset_input import DsiBase, Dsi, DsiCreate, DsiUpdate
from models.parameters import *


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
  commons: dict = Depends(dsi_common_parameters)
  ):
  """ get a paginated list of DSIs """

  time_start = datetime.now()
  query = {
    "dsi_uuid": dsi_uuid,
    **commons,
  }
  print ("query : \n", query)


  ### TO DO / retrieve results given the query 
  # results = 




  ### marshal / apply model to data
  data_list =  [ Dsi(**test_dsi) ]


  time_end = datetime.now()
  stats = {
    'total_items' : len(data_list),
    'queried_at' : str(time_start),  
    'response_at' : str(time_end), 
    'response_delta' : time_end - time_start,  
  }

  if only_data : 
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


@router.get("/{dsi_uuid}")
async def read_dsi( 
  dsi_uuid: uuid.UUID,
  ):
  """ get a specific DSI (without its DSRs) """

  time_start = datetime.now()

  query = {
    "dsi_uuid": dsi_uuid,
  }

  ### TO DO / retrieve results from db and query
  test_dsi_ = {
    'title' : 'test_dsi',
    'dsi_uuid' : dsi_uuid ,
    'owner' : 'system'
  }

  ### marshal / apply model to data
  data =  Dsi(**test_dsi_)


  if only_data : 
    response = ResponseDataBase(
      data =  data,
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



@router.post("/")
async def create_dsi(
  dsi_in: DsiCreate,
  ):

  """ post a new DSI """
  # pp.pprint(dsi_in)

  dsi_client = DsiBase( **dsi_in.dict() )
  dsi_client_dict = dsi_client.dict()

  ### generate a random UUID / cf : https://docs.python.org/3/library/uuid.html
  dsi_client_dict['dsi_uuid'] = uuid.uuid4()
  dsi_db = Dsi(**dsi_client_dict)

  response = ResponseDataBase(
    data = dsi_db
  )
  return response










@router.put("/{dsi_uuid}")
async def update_dsi(
  dsi_uuid: uuid.UUID,
  ):
  """ update a specific DSI """

  return {"dsi_uuid": dsi_uuid}



@router.delete("/{dsi_uuid}")
async def delete_dsi(
  dsi_uuid: uuid.UUID,
  ):
  """ delete a specific DSI """

  return {"dsi_uuid": dsi_uuid}