from log_config import log_, pformat
import inspect 

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
# from fastapi.openapi.docs import get_swagger_ui_html
# from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

from core import config

### cf : https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680

log_.debug(">>> api/api_v1/endpoints/utils/security.py")


API_KEY = config.API_KEY
API_KEY_NAME = config.API_KEY_NAME # "access_token"
COOKIE_DOMAIN = config.COOKIE_DOMAIN # "crudity.me"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
  api_key_query: str = Security(api_key_query),
  api_key_header: str = Security(api_key_header),
  api_key_cookie: str = Security(api_key_cookie),
  ):

  if api_key_query == API_KEY:
    return api_key_query

  elif api_key_header == API_KEY:
    return api_key_header

  elif api_key_cookie == API_KEY:
    return api_key_cookie
    
  else:
    raise HTTPException(
      status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
