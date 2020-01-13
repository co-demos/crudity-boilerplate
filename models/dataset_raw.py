from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel

from models.config import DSR_DOC_TYPE
from models.datalog import DataLogBase



AnyContent = TypeVar('AnyContent')


# Shared properties
class DsrData(BaseModel) : 

  data: AnyContent

  class Config:
  
    schema_extra = {
      'example' : {

        'data' : {
          "field_01": "you can push any data you want",
          "field_02": "either nested or flat structure",
          "field_03": {
            "subfield_A" : "numerical or text...",
            "subfield_B" : "anything...",
            "subfield_C" : {
              "subsubfield_1" : "you need to store...",
              "subsubfield_2" : "... except a field called <_id> !!!"
            },
          },
          "field_04" : 42, 
          "field_05" : True, 
        }
        
      }
    }

class DsrUpdateData(BaseModel) : 

  update_data: AnyContent
  modified_at : Optional[str] = None
  modified_by : Optional[str] = None
  
  class Config:
  
    schema_extra = {
      'example' : {

        'update_data' : {
          "field_01": "this is updated data on field_01",
          "field_02": "my updated field_02 data",
          "field_03": {
            "subfield_A" : "Update data for numerical or text...",
            "subfield_B" : 42,
          }
        }
        
      }
    }


class DsrBase(DsrData) : 

  type: str = DSR_DOC_TYPE
  dsi_uuid: UUID = None

  team: List[ str ] = [] ### additional list of people authorized to modify

  created_by: str = None
  created_at: datetime = None
  updated_at: datetime = None
  logs: List[ DataLogBase ] = []
  
  modified_at : Optional[str] = None
  modified_by : Optional[str] = None

  is_deleted : Optional[bool] = False
  is_test_data : Optional[bool] = False
  

# Properties to receive on item creation
class DsrCreate(DsrBase):

  dsi_uuid: UUID 


# Properties to receive on item update
class DsrUpdate(DsrBase):

  data: AnyContent


# Properties to return to client
class Dsr(DsrBase):

  dsr_uuid: UUID

  data: AnyContent


# Properties properties stored in ES DB
class DsrInDB(DsrBase):

  dsr_uuid: UUID
  dsi_uuid: UUID 

  data: AnyContent


# Properties properties stored in MongoDB
class DsrInMongoDB(DsrInDB):

  is_deleted: bool = False
  version: int
  updated_by: str = None
