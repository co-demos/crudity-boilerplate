from typing import List, Optional, Union, Dict
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel

from models.config import DMF_DOC_TYPE, DMT_DOC_TYPE
from models.opendatalevels import OpenDataLevelEnum, LicenceEnum


class DatamodelFieldBase(BaseModel):

  dmf_uuid: UUID

  type: str = DMF_DOC_TYPE
  title: str = None
  description: str = None

  validations: dict = {}

  source: str = None
  references: List[str] = []

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

  owner: str = 'anonymous'
  team: List[ str ] = []

  created_at: datetime = None
  last_update: datetime = None
  logs: List[ str ] = []


class DatamodelTemplatedBase(BaseModel):
  
  dmt_uuid: UUID

  type: str = DMT_DOC_TYPE
  title: str = None
  description: str = None

  source: str = None
  references: List[str] = []

  datamodel_fields  : List[DatamodelFieldBase] = []

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   OpenDataLevelEnum = OpenDataLevelEnum.private

  owner: str = 'anonymous'
  team: List[ str ] = []

  created_at: datetime = None
  last_update: datetime = None
  logs: List[ str ] = []