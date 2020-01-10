from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel

from models.config import DSI_DOC_TYPE, DMF_DOC_TYPE
from models.datalog import DataLogBase
from models.datamodel import DatamodelFieldBase, DatamodelTemplatedBase
from models.opendatalevels import OpenDataLevelEnum, LicenceEnum



# DSI fields
# class Dsi_user(BaseModel):
  # pass


AnyContent = TypeVar('AnyContent')

class ForeignKey(BaseModel):
  
  key_field_source: str = None
  key_field_target: str = None
  dsi_uuid_target: UUID = None


# Shared properties
class DsiBase(BaseModel) : 

  type: str = DSI_DOC_TYPE
  title: str = None
  description: str = None
  licence: Optional[str] = None
  
  source: str = None
  tags: List[ str ] = []

  is_geodata: bool = False
  has_dsr_data : bool = False
  is_test_data : Optional[bool] = False
  is_deleted : Optional[bool] = False

  datamodel_fields  : List[DatamodelFieldBase] = []
  datamodel_template: DatamodelTemplatedBase = None

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

  owner: str = 'anonymous'
  team: List[ str ] = []

  created_by: str = None
  created_at: datetime = None
  updated_at: datetime = None
  logs: List[ DataLogBase ] = []           ### TO DO : make models for logs

  foreign_keys: List[ ForeignKey ] = [] 


# Properties to receive on item creation
class DsiCreate(BaseModel):

  title: str
  description: str = None
  licence: Optional[str] = None

  is_geodata: bool = False
  has_dsr_data : bool = False

  is_test_data : Optional[bool] = False
  is_deleted : Optional[bool] = False

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

  class Config:

    schema_extra = {
      'example' : {

        "title": "my new dataset input",
        "description": "my dataset input description",
        "licence": "MIT",
        "is_geodata": False,
        "auth_preview": "opendata",
        "auth_modif": "private"
        
      }
    }


# Properties to receive on item update
class DsiUpdate(BaseModel):

  update_data: AnyContent

  class Config:
  
    schema_extra = {
      'example' : {
        
        'update_data' : {
          "title": "my updated dataset input",
          "description": "my updated dataset input description",
          "licence": "my peculiar licence",
          # "is_geodata": False,
          # "auth_preview": "opendata",
          # "auth_modif": "private"
        }
        
      }
    }


# Properties to return to client
class Dsi(DsiBase):

  # dsi_uuid: UUID
  dsi_uuid: str
  # dsi_uuid: int

  title: str
  owner : str


# Properties stored in DB
class DsiInDB(DsiBase):

  dsi_uuid: UUID


class DsiInMongoDB(DsiInDB):

  version: int
  is_deleted: bool = False
  updated_by: str = None



class DsiEs(BaseModel):
  _index: str
  # _type: str
  # _id: str
  # _score: float
  _source: AnyContent


class DsiList(BaseModel):
  dsis : List[ Dsi ]

class DsiESList(BaseModel):
  # __root__ : List[ DsiEs ]
  dsis : List[ DsiEs ]
