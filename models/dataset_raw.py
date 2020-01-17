from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel

from models.config import DSR_DOC_TYPE
from models.datalog import DataLogBase, Comment
from models.opendatalevels import OpenDataLevelEnum, EditLevelEnum, LicenceEnum
from models.user import TeamMember, TeamMemberIn



AnyContent = TypeVar('AnyContent')


# Shared properties


class DsrOptional(BaseModel): 

  licence:       Optional[ Union[ str, LicenceEnum ] ] = None
  source:        Optional[ str ] = None

  team:          Optional[List[ TeamMember ]] = []

  comments:      Optional[ List[ Comment ] ] = None 

  is_test_data : Optional[bool] = False


class DsrOptionalPlus(DsrOptional) : 

  modified_at :  Optional[datetime] = None
  modified_by :  Optional[str] = None

  is_deleted :   Optional[bool] = False

  auth_preview:  Optional[OpenDataLevelEnum] = OpenDataLevelEnum.opendata
  auth_modif:    Optional[EditLevelEnum] = EditLevelEnum.private



class DsrData(DsrOptional) : 

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   EditLevelEnum = EditLevelEnum.private

  data: AnyContent

  # is_test_data : Optional[bool] = False

  class Config:
  
    schema_extra = {
      'example' : {

        'auth_preview' : 'opendata',
        'auth_modif' : 'private',

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


# class DsrUpdateData(BaseModel) : 
class DsrUpdateData(BaseModel) : 

  update_data: AnyContent

  # team: Optional[List[ TeamMember ]] = []

  # modified_at : Optional[datetime] = None
  # modified_by : Optional[str] = None
  
  class Config:
  
    schema_extra = {
      'example' : {

        'update_data' : {
          'source' : 'my new source',
          'licence' : 'Obbl-42',
          "auth_preview": "commons",
          "auth_modif": "team",
          'data' : {
            "field_01": "this is updated data on field_01",
            "field_02": "my updated field_02 data",
            "field_03": {
              "subfield_A" : "Update data for numerical or text...",
              "subfield_B" : 42,
            }
          }
        }
        
      }
    }


class DsrUpdateDataIn(DsrOptionalPlus) : 

  data : AnyContent 



class DsrBase(DsrData) : 

  type: str = DSR_DOC_TYPE

  # dsi_uuid: UUID = None
  dsi_uuid: str = None

  # licence: Optional[ Union[ str, LicenceEnum ] ] = None
  # source:  Optional[ str ] = None

  is_deleted : Optional[bool] = False
  is_test_data : Optional[bool] = False

  # auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  # auth_modif:   EditLevelEnum = EditLevelEnum.private

  owner: str = 'anonymous'
  team: List[ TeamMember ] = [] ### additional list of people authorized to modify

  created_by: str = None
  created_at: datetime = None

  # updated_at: datetime = None
  logs: List[ DataLogBase ] = []
  
  modified_at : Optional[str] = None
  modified_by : Optional[str] = None
  
  # comments: Optional[ List[ Comment ] ] = None 


# Properties to receive on item creation
class DsrCreate(DsrBase):

  # dsi_uuid: UUID 
  dsi_uuid: str       ### make it mandatory


# Properties to receive on item update
class DsrUpdate(DsrBase):

  data: AnyContent


# Properties to return to client
class Dsr(DsrBase):

  # dsr_uuid: UUID
  dsr_uuid: str

  data: AnyContent


# Properties properties stored in ES DB
class DsrInDB(DsrBase):

  # dsr_uuid: UUID
  # dsi_uuid: UUID 

  dsr_uuid: str
  dsi_uuid: str 

  data: AnyContent


# Properties properties stored in MongoDB
class DsrInMongoDB(DsrInDB):

  is_deleted: bool = False
  version: int
  updated_by: str = None
