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


class DsrBase(DsrData) : 

  type: str = DSR_DOC_TYPE
  dsi_uuid: UUID = None

  team: List[ str ] = [] ### additional list of people authorized to modify

  created_by: str = None
  created_at: datetime = None
  updated_at: datetime = None
  logs: List[ DataLogBase ] = []



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
