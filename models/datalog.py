from typing import List, Optional, Union, Dict, TypeVar
from enum import Enum, IntEnum
from datetime import date, datetime, time, timedelta
from uuid import UUID

from pydantic import BaseModel



class DataLogBase(BaseModel):
  
  created_by: str = None
  created_at: datetime = None
  updated_at: datetime = None

