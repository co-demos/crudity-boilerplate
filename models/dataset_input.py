from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel

from models.config import DSI_DOC_TYPE, DMF_DOC_TYPE
from models.datamodel import DatamodelFieldBase, DatamodelTemplatedBase
from models.opendatalevels import OpenDataLevelEnum, LicenceEnum



# DSI fields
# class Dsi_user(BaseModel):
  # pass


# Shared properties
class DsiBase(BaseModel) : 

  type: str = DSI_DOC_TYPE
  title: str = None
  description: str = None
  licence: Optional[str] = None
  source: str = None
  tags: List[ str ] = []

  datamodel_fields  : List[DatamodelFieldBase] = []
  datamodel_template: DatamodelTemplatedBase = None

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

  owner: str = 'anonymous'
  team: List[ str ] = []

  created_at: datetime = None
  last_update: datetime = None
  logs: List[ str ] = []


# Properties to receive on item creation
class DsiCreate(BaseModel):

  title: str
  description: str = None

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

# Properties to receive on item update
class DsiUpdate(DsiBase):
  pass


# Properties to return to client
class Dsi(DsiBase):

  dsi_uuid: UUID              ### mandatory
  title: str
  owner : str


# Properties properties stored in DB
class DsiInDB(DsiBase):
  dsi_uuid: UUID
  title: str
