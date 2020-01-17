from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum

from pydantic import BaseModel

from models.config import DSI_DOC_TYPE, DSR_DOC_TYPE, DMF_DOC_TYPE, DMT_DOC_TYPE
from models.opendatalevels import OpenDataLevelEnum, EditLevelEnum
from models.user import TeamMember


class DocTypeEnum(str, Enum) :

  dsi = DSI_DOC_TYPE
  dsr = DSR_DOC_TYPE
  dmt = DMT_DOC_TYPE
  dmf = DMF_DOC_TYPE


class DocAuthData(BaseModel):
  
  type: DocTypeEnum = DSI_DOC_TYPE

  auth_preview: OpenDataLevelEnum = OpenDataLevelEnum.opendata
  auth_modif:   EditLevelEnum = EditLevelEnum.private

  owner: str = 'anonymous'
  team: List[ TeamMember ] = []
