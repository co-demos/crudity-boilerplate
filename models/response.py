from typing import List, Optional, Union, Dict, TypeVar
from datetime import date, datetime, time, timedelta

from pydantic import BaseModel



AnyContent = TypeVar('AnyContent')

# Shared properties
class ResponseDataBase(BaseModel) : 

  data: AnyContent = None

class ResponseStatsNoTotal(BaseModel) :
  
  queried_at: datetime = None
  response_at: datetime = None
  response_delta: timedelta = None

class ResponseStats(ResponseStatsNoTotal) :

  total_items: int = None


class ResponseBase(ResponseDataBase) : 

  status: str = 200

  query: AnyContent
  stats: ResponseStats


class ResponseBaseNoTotal(ResponseDataBase) : 

  status: str = 200

  query: AnyContent
  stats: ResponseStatsNoTotal