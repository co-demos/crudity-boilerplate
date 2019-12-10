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


test_dsi = {
  'title' : 'test_dsi',
  'dsi_uuid' : 'd7b0cd1b-599a-4f3e-8820-9acc8e1d59e6',
  'owner' : 'system'

}



router = APIRouter()

# @router.get("/list", response_model=List[Dsi])
@router.get("/list")
async def list_dsis(

  q: list = query_str, 
  filter: list = search_filter, 
  item_uuid: list = item_uuid,

  page: int = page_number,
  per_page: int = per_page,
  sort_by: str = sort_by,  
  sort_order: str = sort_order,   
  shuffle_seed: int = shuffle_seed,  

  field_to_return: list = field_to_return, 
  fields_to_return: str = fields_to_return,

  data_format : str = data_format,
  only_data: bool = only_data,

  for_map: bool = for_map, 

):
  # return {"message": "Hello World"}

  time_start = datetime.now()
  query = {

    "item_uuid": item_uuid,
    "q" : q,
    "filter" : filter,

    "field_to_return" : field_to_return,
    "fields_to_return" : fields_to_return,

    "page" : page,
    "per_page" : per_page,
    "sort_by" : sort_by, 
    "sort_order" : sort_order, 
    "shuffle_seed" : shuffle_seed, 

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


# @router.get("/{dsi_uuid}/search")
# async def search_dsi(dsi_uuid):
#   return {"dsi_uuid": dsi_uuid}


@router.get("/{dsi_uuid}")
async def read_dsi( 

  dsi_uuid: uuid.UUID,

  field_to_return: list = field_to_return, 
  fields_to_return: str = fields_to_return,

  data_format : str = data_format,
  only_data: bool = only_data, 

  ):

  time_start = datetime.now()

  query = {

    "dsi_uuid": dsi_uuid,

    "field_to_return" : field_to_return,
    "fields_to_return" : fields_to_return,

  }



  test_dsi_ = {
    'title' : 'test_dsi',
    'dsi_uuid' : dsi_uuid ,
    'owner_username' : 'system'
  }

  ### marshal / apply model to data
  data =  Dsi(**test_dsi_)

  time_end = datetime.now()
  stats = {
    'total_items' : len([data]),
    'queried_at' : str(time_start),  
    'response_at' : str(time_end), 
    'response_delta' : time_end - time_start,  
  }

  if only_data : 
    response = ResponseDataBase(
      data =  data,
    )
  else : 
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

  pp.pprint(dsi_in)

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
  dsi_uuid: str,
  ):
  return {"dsi_uuid": dsi_uuid}



@router.delete("/{dsi_uuid}")
async def delete_dsi(
  dsi_uuid: str,
  ):
  return {"dsi_uuid": dsi_uuid}