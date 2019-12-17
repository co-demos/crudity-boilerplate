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

from models.user import UserLogin
from models.response import ResponseBase, ResponseDataBase, ResponseBaseNoTotal


from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from api.utils.security import get_api_key, API_KEY_NAME, COOKIE_DOMAIN


import crud

print()
log_.debug(">>> api/api_v1/endpoints/login.py")


from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)


router = APIRouter()



@router.post("/login")
async def post_login(
  *, 
  user_login: UserLogin = Body(..., embed=True), 
  api_key: APIKey = Depends(get_api_key)
  ):
  response = "How cool is this?"
  return response

@router.get("/logout")
async def get_logout(
  api_key: APIKey = Depends(get_api_key)
  ):
  response = "How cool is this?"
  return response
