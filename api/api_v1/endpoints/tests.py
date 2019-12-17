from log_config import log_, pformat
import inspect 

from typing import List, Dict, Optional
from datetime import date, datetime, time, timedelta
import uuid

from pydantic import ValidationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import Response, RedirectResponse, JSONResponse
from starlette.status import *

from models.response import ResponseBase, ResponseDataBase, ResponseBaseNoTotal

from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from api.utils.security import get_api_key, API_KEY_NAME, COOKIE_DOMAIN


import crud

print()
log_.debug(">>> api/api_v1/endpoints/login.py")


from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)


router = APIRouter()



@router.get("/openapi.json")
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
  response = JSONResponse(
    get_openapi(title="FastAPI security test", version=1, routes=router.routes)
  )
  return response


@router.get("/documentation")
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
  response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
  response.set_cookie(
    API_KEY_NAME,
    value=api_key,
    domain=COOKIE_DOMAIN,
    httponly=True,
    max_age=1800,
    expires=1800,
  )
  return response


@router.get("/secure_endpoint")
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
  response = "How cool is this?"
  return response

