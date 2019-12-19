from log_config import log_, pformat
import inspect 

from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.responses import Response, RedirectResponse, JSONResponse
from starlette.status import *
from starlette.requests import Request

from models.user import UserLogin
from models.response import ResponseBase, ResponseDataBase, ResponseBaseNoTotal
from models.parameters import p_auth_token, p_access_token


from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from api.utils.security import get_api_key, \
  API_KEY_NAME, COOKIE_DOMAIN, distantAuthCall
  # getApiKey, getApiKey_mandatory, getApiKey_optional


import crud
from core import config
AUTH_MODE = config.AUTH_MODE


print()
log_.debug(">>> api/api_v1/endpoints/login.py")


from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)


router = APIRouter()



@router.get("/anonymous_login")
async def anonymous_login(
  resp_: Response,
  request : Request,
  ):

  """ 
  Gets an anonymous access_token
  """ 

  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "GET / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  # response = "How cool is this?"

  resp_login_anon = distantAuthCall(
    api_request=None, 
    query={}, 
    payload={}, 
    func_name='login_anonymous'
  )

  return resp_login_anon


@router.post("/login")
async def post_login_infos(
  *, 
  resp_: Response,
  request : Request,
  # access_token: str = p_access_token,
  user_login: UserLogin = Body(..., embed=True), 
  api_key: APIKey = Depends(get_api_key),
  ):

  """ 
  Needs an anonymous access_token
  """ 
  ### DEBUGGING
  print()
  print("-+- "*40)
  log_.debug( "POST / %s", inspect.stack()[0][3] )
  time_start = datetime.now()

  log_.debug( "user_login : \n%s", pformat(user_login.dict()) )
  log_.debug( "request : \n%s", pformat(request.__dict__) )

  resp_login = distantAuthCall(
    api_request=request, 
    query={}, 
    payload={ **user_login.dict() }, 
    func_name='login_user',
    token=api_key
  )

  return resp_login



# @router.get("/logout")
# async def get_logout(
#   resp_: Response,
#   request : Request,
#   api_key: APIKey = Depends(getApiKey_mandatory)
#   ):

#   ### DEBUGGING
#   print()
#   print("-+- "*40)
#   log_.debug( "POST / %s", inspect.stack()[0][3] )
#   time_start = datetime.now()

#   log_.debug( "api_key : \n%s", pformat(api_key.__dict__ ) )

#   return api_key
