from typing import List, Optional, Union, Dict, TypeVar
from datetime import date, datetime, time, timedelta

from pydantic import BaseModel



AnyContent = TypeVar('AnyContent')

class ResponseStatus(BaseModel) : 

  status_code: str = 200
  error: str = None
  info: dict = None


# Shared properties
class ResponseDataBase(BaseModel) : 

  status: ResponseStatus = None
  data: AnyContent = None

class ResponseStatsNoTotal(BaseModel) :
  
  queried_at: datetime = None
  response_at: datetime = None
  response_delta: timedelta = None

class ResponseStats(ResponseStatsNoTotal) :

  total_items: int = None


class ResponseBase(ResponseDataBase) : 

  query: AnyContent
  stats: ResponseStats


class ResponseBaseNoTotal(ResponseDataBase) : 

  query: AnyContent
  stats: ResponseStatsNoTotal