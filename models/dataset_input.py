from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel

from models.config import DSI_DOC_TYPE, DMF_DOC_TYPE
from models.datalog import DataLogBase, Comment
from models.opendatalevels import OpenDataLevelEnum, EditLevelEnum, LicenceEnum
from models.user import TeamMember, TeamMemberIn

from models.datamodel import DatamodelFieldBase, DatamodelTemplatedBase



# DSI fields
# class Dsi_user(BaseModel):
  # pass


AnyContent = TypeVar('AnyContent')

class ForeignKey(BaseModel):
  
  key_field_source: str = None
  key_field_target: str = None
  # dsi_uuid_target: UUID = None
  dsi_uuid_target: str = None

  class Config:
  
    schema_extra = {
      'example' : {
        'key_field_source' : 'my-source-field',
        'key_field_target' : 'my-target-field',
        'dsi_uuid_target' : '1234567890',
      }
    }

# Shared properties

class DsiOptionnal(BaseModel) :

  licence:       Optional[ Union[ str, LicenceEnum ] ] = None
  is_test_data : Optional[ bool ] = False
  # is_deleted :   Optional[ bool ] = False
  # modified_at :  Optional[ datetime ] = None
  # modified_by :  Optional[ str ] = None


class DsiOptionalPlus(DsiOptionnal) : 

  is_deleted :   Optional[ bool ] = False
  modified_at :  Optional[ datetime ] = None
  modified_by :  Optional[ str ] = None


class DsiBase(DsiOptionalPlus) : 

  type: str = DSI_DOC_TYPE
  title: str = None
  description: str = None
  # licence: Optional[ Union[ str, LicenceEnum ] ] = None
  
  source: str = None
  tags: List[ str ] = []

  is_geodata: bool = False
  has_dsr_data : bool = False
  # is_test_data : Optional[bool] = False
  # is_deleted : Optional[bool] = False

  datamodel_fields  : List[ DatamodelFieldBase ] = []
  datamodel_template: DatamodelTemplatedBase = None

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   EditLevelEnum = EditLevelEnum.private

  owner: str = 'anonymous'
  team: List[ TeamMember ] = []

  created_by: str = None
  created_at: datetime = None
  updated_at: datetime = None
  logs: Union[None, List[ DataLogBase ]] = []           ### TO DO : make models for logs

  foreign_keys: List[ ForeignKey ] = [] 

  # modified_at : Optional[str] = None
  # modified_by : Optional[str] = None

  # comments: Optional[ List[Comment] ] = []
  comments: Union[None, List[Comment]] = [] 


# Properties to receive on item creation
class DsiCreate(DsiOptionnal):

  title: str
  description: str = None
  # licence: Optional[ Union[ str, LicenceEnum ] ] = None

  is_geodata: bool = False
  has_dsr_data : bool = False

  # is_test_data : Optional[bool] = False
  # is_deleted : Optional[bool] = False

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

  team: Optional[List[ TeamMember ]] = []

  comments: Optional[ List[ Comment ] ] = [] 

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

  # modified_by : Optional[ str ] = None
  # modified_at : Optional[ datetime ] = None

  class Config:
  
    schema_extra = {
      'example' : {
        
        'update_data' : {
          "title": "my updated dataset input",
          "description": "my updated dataset input description",
          "licence": "my peculiar licence",

          "is_geodata": False,
          "auth_preview": "commons",
          "auth_modif": "team",

          'team': [{
            "email": "test@email.com",
            "roles": [ 
              "read", 
              "comment", 
              "edit", 
              "delete" 
            ],
          }],

        }
        
      }
    }


class DsiUpdateIn(DsiOptionnal) :
  # type:               Optional[str] = DSI_DOC_TYPE
  title:              Optional[str] = None
  description:        Optional[str] = None
  source:             Optional[str] = None
  tags:               Optional[List[ str ]] = []
  is_geodata:         Optional[bool] = False
  has_dsr_data :      Optional[bool] = False
  datamodel_fields  : Optional[List[ DatamodelFieldBase ]] = []
  datamodel_template: Optional[DatamodelTemplatedBase] = None
  auth_preview:       Optional[OpenDataLevelEnum] = OpenDataLevelEnum.opendata
  auth_modif:         Optional[EditLevelEnum] = EditLevelEnum.private
  owner:              Optional[str] = 'anonymous'
  team:               Optional[List[ TeamMember ]] = []
  # created_by:         Optional[str] = None
  # created_at:         Optional[datetime] = None
  updated_at:         Optional[datetime] = None
  # logs:               Optional[List[ DataLogBase ]] = []           ### TO DO : make models for logs
  foreign_keys:       Optional[List[ ForeignKey ]] = [] 
  comments:           Optional[List[ Comment ]] = []

  class Config:
    
    schema_extra = {
      'example' : {
        
          "title": "my updated dataset input",
          "description": "my updated dataset input description",
          "licence": "my peculiar licence",

          "is_geodata": False,
          "auth_preview": "commons",
          "auth_modif": "team",

          'team': [{
            "email": "test@email.com",
            "roles": [ 
              "read", 
              "comment", 
              "edit", 
              "delete" 
            ],
          }],

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
