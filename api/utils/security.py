from log_config import log_, pformat
import inspect 

import requests
import json

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
# from fastapi.openapi.docs import get_swagger_ui_html
# from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

from config.auth_distant_protocols import functions_protocols
from core import config

### cf : https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680

log_.debug(">>> api/api_v1/endpoints/utils/security.py")


API_KEY = config.API_KEY
# API_KEY_QUERY = config.API_KEY_QUERY
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

  log_.debug("api_key_query : %s", api_key_query )
  log_.debug("api_key_header : %s", api_key_header )
  log_.debug("api_key_cookie : %s", api_key_cookie )

  if api_key_query : # == API_KEY:
    return api_key_query
  elif api_key_header : # == API_KEY:
    return api_key_header
  elif api_key_cookie : # == API_KEY:
    return api_key_cookie
  else:
    raise HTTPException(
      status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


async def get_api_key_optional(
  api_key_query: str = Security(api_key_query),
  api_key_header: str = Security(api_key_header),
  api_key_cookie: str = Security(api_key_cookie),
  ):

  if api_key_query : 
    return api_key_query
  elif api_key_header : 
    return api_key_header
  elif api_key_cookie : 
    return api_key_cookie
  else:
    return None



# def getTokenFromRequest(api_request) : 
#   """ 
#   retrieve token sent with request 
#   """ 

#   log_.debug("getTokenFromRequest ..." )
#   log_.debug("getTokenFromRequest / api_request : \n%s", pformat(api_request) )

#   # token_header_location = config.JWT_HEADER_NAME
#   token_header_location = config.API_KEY_NAME
#   log_.debug("getTokenFromRequest / token_header_location : %s", token_header_location )
#   try : 
#     token_from_headers = api_request['headers'].get(token_header_location, None)
#     log_.debug("getTokenFromRequest / token_from_headers : %s", token_from_headers )
#   except : 
#     token_from_headers = None 

#   # token_query_string = config.JWT_QUERY_STRING_NAME
#   token_query_string = config.API_KEY_NAME
#   log_.debug("getTokenFromRequest / token_query_string : %s", token_query_string )
#   try : 
#     token_from_query = api_request['query_string'].get(token_query_string, None)
#     log_.debug("getTokenFromRequest / token_from_query : %s", token_from_query )
#   except : 
#     token_from_query = None 

#   if token_from_headers or token_from_query : 
#     return token_from_headers if token_from_headers else token_from_query
#   else : 
#     return None


def getDistantAuthUrl():
  """ 
  """

  auth_mode = config.AUTH_MODE
  log_.debug("getDistantAuthUrl / auth_mode : %s", auth_mode )

  if auth_mode != 'internal' : 

    auth_url_root_modes = {
      "default" : config.AUTH_URL_ROOT_LOCAL,
      "dev" : config.AUTH_URL_ROOT_LOCAL,
      "local" : config.AUTH_URL_ROOT_LOCAL,
      "distant_prod" : config.AUTH_URL_ROOT_DISTANT_PROD,
      "distant_preprod" : config.AUTH_URL_ROOT_DISTANT_PREPOD,
    }

    auth_url_root = auth_url_root_modes[auth_mode]
    # log_.debug("getDistantAuthUrl / auth_url_root : %s", auth_url_root )

    return auth_url_root
  
  else :
    return False


def getDistantEndpointconfig (func_name) : 
  """ 
  """ 
  # print (". "*50)

  func_protocol = functions_protocols[func_name]
  field = func_protocol["endpoint_config"]
  subfield = func_protocol["endpoint_code"]

  auth_dist_configs = config.AUTH_DISTANT_ENDPOINTS
  endpoint_config = auth_dist_configs[field][subfield] 

  return endpoint_config


def distantAuthCall ( 
  api_request=None, 
  query={}, 
  payload={}, 
  func_name='login_user',
  token=None,
  ) :
  """ 
  sending request to the distant auth url / service 
  specified in config + env vars
  """

  print (". "*50)
  log_.debug("distantAuthCall/ payload : \n%s", pformat(payload) )
  log_.debug("distantAuthCall/ log_type : %s", func_name )

  ### retrieve distant auth url root
  auth_url_root = getDistantAuthUrl()
  log_.debug("distantAuthCall/ auth_url_root : %s", auth_url_root )

  ### retrieve distant auth endpoint config
  endpoint_config = getDistantEndpointconfig(func_name)
  log_.debug("distantAuthCall/ endpoint_config : \n%s", pformat(endpoint_config) )
  
  url = endpoint_config["url"]
  method = endpoint_config["method"]
  url_args = endpoint_config["url_args"]
  post_args = endpoint_config["post_args"]
  url_append = endpoint_config["url_append"]
  resp_path = endpoint_config["resp_path"]


  ### build url base for specific auth
  base_url = auth_url_root + url 
  log_.debug("distantAuthCall/ base_url : %s", base_url )




  ### TO DO : append url_append value
  # get param from request
  log_.debug("distantAuthCall / url_append : %s", url_append )
  if url_append : 
    # log_.debug("distantAuthCall / api_request : \n%s", pformat(api_request.__dict__) )
    url_append_string = ""
    url_append_list = []
    view_args = api_request.view_args
    log_.debug("distantAuthCall / view_args : \n%s", pformat(view_args) )
    for append_arg in url_append : 
      append_val = view_args[append_arg]
      url_append_list.append(append_val)
    url_append_string = "/".join(url_append_list)
    base_url += url_append_string





  ### append distant auth request headers
  headers = config.AUTH_URL_HEADERS
  if payload :
    headers = config.AUTH_URL_HEADERS_PAYLOAD

  ### add token to requests in headers or query_string
  # token = None
  # if api_request :
    # token = getTokenFromRequest(api_request)
  log_.debug("token : %s", token )

  token_query_string = ""

  if token :
    token_locations = config.AUTH_URL_TOKEN_LOCATION
    
    if "query_string" in token_locations and  "headers" not in token_locations : 
      token_query_string_name = config.AUTH_URL_TOKEN_QUERY_STRING_NAME
      token_query_string = "{}={}".format(token_query_string_name,token)

    if "headers" in token_locations : 
      token_header_name = config.AUTH_URL_TOKEN_HEADER_NAME
      token_header_type = config.AUTH_URL_TOKEN_HEADER_TYPE
      headers[token_header_name] = token

  log_.debug("distantAuthCall / headers : \n%s", pformat(headers) )




  ### TO DO : append url_args
  url_args_string = ""
  if url_args :
    url_args_string = "?"
    for arg_k, arg_v in url_args.items() : 
      url_args_string += "&{}={}".format( arg_k, query[arg_v]  )
  query_url = base_url + url_args_string + token_query_string
  log_.debug("distantAuthCall / query_url : %s", query_url)



  ### send request to service and read response
  if method == 'GET' : 
    response = requests.get(query_url, headers=headers)

  elif method == 'DELETE' : 
    response = requests.delete(query_url, headers=headers)

  elif method in ['POST', 'PUT'] :

    ### rebuild payload given 

    # remap payload given endpoint connfig 
    payload_type = type(payload)
    log_.debug("distantAuthCall / payload_type : %s", payload_type )
    
    if post_args : 
      if payload_type == dict : 
        payload_remapped = {
          post_args[k] : v for k,v in payload.items() if k in post_args.keys()
        }
      elif payload_type == list : 
        payload_remapped = []
        for p in payload : 
          p_remapped = {
            post_args[k] : v for k,v in p.items() if k in post_args.keys()
          }
          payload_remapped.append(p_remapped)
    else : 
      payload_remapped = payload
    log_.debug("distantAuthCall / payload_remapped : \n%s", pformat(payload_remapped) )

    # then payload as json
    payload_json = json.dumps(payload_remapped)
    log_.debug("distantAuthCall / payload_json : %s", payload_json )

    if method == 'POST' : 
      response = requests.post(query_url, data=payload_json, headers=headers)

    elif method == 'PUT' : 
      response = requests.put(query_url, data=payload_json, headers=headers)


  log_.debug("distantAuthCall / response.status_code : %s", response.status_code )
  log_.debug("distantAuthCall / response : \n%s", response.__dict__ )
  if response.status_code == 200 :
    response_json = response.json()
  else : 
    response_ = response.__dict__
    response_json = {
      'status_code' : response_['status_code'],
      'url' : response_['url'],
      'content' : response_['_content'],
      'headers' : response_['headers'],
    }
  log_.debug("distantAuthCall / response_json : \n%s", pformat(response_json) )
  
  if resp_path and response.status_code == 200 : 
    ### remap response_json given resp_path if specific 
    response_json = { arg_k : response_json[arg_v] for arg_k, arg_v in resp_path.items() if arg_v in response_json.keys() }

  return response_json


