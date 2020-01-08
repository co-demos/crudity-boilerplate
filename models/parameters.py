from enum import Enum, IntEnum
from pydantic import BaseModel

from fastapi import Query, Depends, Path


### COMMON SEARCH PARAMETERS

p_query_str = Query(
  None, ### default value
  alias="search_for",
  title="Query string",
  description="`str`: Query string for the items to search in the database that have a good match",
  # min_length=3,
  # max_length=50,
  # regex="^fixedquery$",
  # deprecated=True,
)

p_item_uuid = Query(
  None, 
  alias="item_uuid",
  title="Item UUID",
  description="`str`: Item UUID to retrieve",
)

p_dsi_uuid = Query(
  None, 
  alias="dsi_uuid",
  title="DSI UUID",
  description="`str`: UUID to retrieve a DSI",
)

p_dsr_uuid = Query(
  None, 
  alias="dsr_uuid",
  title="DSR UUID",
  description="`str`: UUID to retrieve a DSR",
)

### AUTH
p_auth_token = Query(
  None, 
  alias="auth_token",
  title="Authorization token",
  description="`str`: Auth token (usually access token)",
)

p_access_token = Query(
  None, 
  alias="access_token",
  title="Access token",
  description="`str`: Access token",
)


p_search_filter = Query (
  None, 
  alias="filter",
  title="Search filter",
  description="`str`: Filter results with this `<field_name>:<field_value>` (use `:` as a seaparator)",
)

### PAGINATION
p_page_number = Query(
  1, 
  alias="page_n",
  title="Page number",
  description="`int`: Page number of the results",
)

class PerPageEnum(IntEnum) :
  min = 1
  pp5 = 5
  pp10 = 10
  pp20 = 20
  pp25 = 25
  pp30 = 30
  pp50 = 50
  pp75 = 75
  pp100 = 100
  pp150 = 150
  pp200 = 200
  pp250 = 250
  pp500 = 500
  pp750 = 750
  pp1000 = 1000
  pp2500 = 2500
  pp5000 = 5000
  pp7500 = 7500
  max = 10000

p_per_page = Query(
  10, 
  alias="per_page",
  title="Results per page",
  description="`int`: Number of results per page",
)
p_sort_by = Query(
  None, 
  alias="sort_by",
  title="Sort by field",
  description="`str`: Field to sort by",
)

class OrderEnum(str, Enum) :
  asc = 'asc'
  desc = 'desc'

p_sort_order = Query(
  'asc', 
  alias="sort_order",
  title="Sort order field",
  description="`str`: Sort order for results",
)
p_shuffle_seed = Query(
  None, 
  alias="shuffle_seed",
  title="Shuffle seed",
  description="`int`: Shuffle seed to shuffle results",
)


class VersionsEnum(str, Enum) :
  last = 'last'
  previous = 'previous'
  first = 'first'
  last10 = 'last10'
  all = 'all'

p_version = Query(
  'last', 
  alias="version",
  title="Data version",
  description="`str`: version of the data requested",
)


class DataFormats(str, Enum) :
  json = 'json'
  geojson = 'geojson'

p_data_format = Query(
  'json', 
  alias="data_format",
  title="Data format",
  description="`str`: format results",
)

p_for_map = Query(
  False, 
  alias="for_map",
  title="For map",
  description="`bool`: format results for map",
)



p_field_to_return = Query(
  None, 
  alias="field_to_return",
  title="Field to return",
  description="`str`: Field to return",
)

p_fields_to_return = Query(
  None, 
  alias="fields_to_return",
  title="Fields to return",
  description="`str`: Fields to return. Separate the fields by a comma after the parameter : `&fields_to_return=<field_A>,<field_B>`",
)

p_full_remove = Query(
  False, 
  alias="full_remove",
  title="full_remove",
  description="`bool`: Completly remove data if `True`, no coming back",
)



p_only_data = Query(
  False, 
  alias="only_data",
  title="Only data",
  description="`bool`: Response only contains results data",
)

p_normalize_data = Query(
  False, 
  alias="normalize_data",
  title="Normalize data",
  description="`bool`: normalize uploaded data",
)

p_get_foreign = Query(
  False, 
  alias="get_linked_data",
  title="Get linked data",
  description="`bool`: append linked data from foreign keys",
)



### dependencies injection

async def query_parameters(
  q: list = p_query_str, 
  version: VersionsEnum = p_version,
  filter: list = p_search_filter, 
  ):
  return {
    "q" : q,
    "version" : version,
    "filter" : filter,
  }


async def tokens_parameters(
  access_token: str = p_access_token, 
  auth_token: str = p_auth_token, 
  ):
  return {
    "access_token" : access_token,
    "auth_token" : auth_token,
  }

async def version_parameters(
  version: VersionsEnum = p_version,
  ):
  return {
    "version" : version,
  }

async def pagination_parameters(
  page_n: int = p_page_number,
  per_page: PerPageEnum = p_per_page,
  sort_by: str = p_sort_by,  
  sort_order: OrderEnum = p_sort_order,   
  shuffle_seed: int = p_shuffle_seed,  
  ):
  return {
    "page_n" : page_n,
    "per_page" : per_page,
    "sort_by" : sort_by, 
    "sort_order" : sort_order, 
    "shuffle_seed" : shuffle_seed, 
  }

async def fields_parameters(
  field_to_return: list = p_field_to_return, 
  fields_to_return: str = p_fields_to_return,
  ):
  return {
    "field_to_return" : field_to_return,
    "fields_to_return" : fields_to_return,
  }

async def format_parameters(
  data_format : DataFormats = p_data_format,
  normalize : bool = p_normalize_data,
  for_map: bool = p_for_map, 
  ):
  return {
    "data_format" : data_format,
    "normalize" : normalize,
    "for_map" : for_map,
  }

async def consolidate_parameters(
  get_foreign : bool = p_get_foreign,
  ):
  return {
    "get_foreign" : get_foreign,
  }

async def resp_parameters(
  only_data: bool = p_only_data,
  ):
  return {
    "only_data" : only_data,
  }

async def delete_parameters(
  full_remove: bool = p_full_remove,
  ):
  return {
    "full_remove" : full_remove,
  }





async def common_parameters(
  query_p: dict = Depends(query_parameters),
  version_p: dict = Depends(version_parameters),
  pagination_p: dict = Depends(pagination_parameters),
  fields_p: dict = Depends(fields_parameters),
  format_p: dict = Depends(format_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **query_p,
    **version_p,
    **pagination_p,
    **fields_p,
    **format_p,
    **resp_p,
  }


async def common_parameters_light(
  query_p: dict = Depends(query_parameters),
  version_p: dict = Depends(version_parameters),
  pagination_p: dict = Depends(pagination_parameters),
  format_p: dict = Depends(format_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **query_p,
    **version_p,
    **pagination_p,
    **format_p,
    **resp_p,
  }

async def common_parameters(
  query_p: dict = Depends(query_parameters),
  version_p: dict = Depends(version_parameters),
  pagination_p: dict = Depends(pagination_parameters),
  fields_p: dict = Depends(fields_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **query_p,
    **version_p,
    **pagination_p,
    **fields_p,
    **resp_p,
  }

async def one_doc_parameters(
  version_p: dict = Depends(version_parameters),
  format_p: dict = Depends(format_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **version_p,
    **format_p,
    **resp_p,
  }

async def one_dsi_parameters(
  version_p: dict = Depends(version_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **version_p,
    **resp_p,
  }

async def search_dsrs_parameters(
  query_p: dict = Depends(query_parameters),
  version_p: dict = Depends(version_parameters),
  pagination_p: dict = Depends(pagination_parameters),
  fields_p: dict = Depends(fields_parameters),
  format_p: dict = Depends(format_parameters),
  consolidate_p: dict = Depends(consolidate_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **query_p,
    **version_p,
    **pagination_p,
    **fields_p,
    **format_p,
    **consolidate_p,
    **resp_p,
  }

async def one_dsr_parameters(
  version_p: dict = Depends(version_parameters),
  fields_p: dict = Depends(fields_parameters),
  format_p: dict = Depends(format_parameters),
  consolidate_p: dict = Depends(consolidate_parameters),
  resp_p: dict = Depends(resp_parameters),
  ):
  return {
    **version_p,
    **fields_p,
    **format_p,
    **consolidate_p,
    **resp_p,
  }