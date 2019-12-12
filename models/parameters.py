from enum import Enum, IntEnum
from pydantic import BaseModel

from fastapi import Query, Depends


### COMMON SEARCH PARAMETERS

query_str = Query(
  None, ### default value
  alias="search_for",
  title="Query string",
  description="`str`: Query string for the items to search in the database that have a good match",
  # min_length=3,
  # max_length=50,
  # regex="^fixedquery$",
  # deprecated=True,
)

item_uuid = Query(
  None, 
  alias="item_uuid",
  title="Item UUID",
  description="`str`: Item UUID to retrieve",
)

dsi_uuid = Query(
  None, 
  alias="dsi_uuid",
  title="DSI UUID",
  description="`str`: UUID to retrieve a DSI",
)

dsr_uuid = Query(
  None, 
  alias="dsr_uuid",
  title="DSR UUID",
  description="`str`: UUID to retrieve a DSR",
)

auth_token = Query(
  None, 
  alias="auth_token",
  title="Authorization token",
  description="`str`: Auth token (usually access token)",
)

only_data = Query(
  False, 
  alias="only_data",
  title="Only data",
  description="`bool`: Response only contains results data",
)

search_filter = Query (
  None, 
  alias="filter",
  title="Search filter",
  description="`str`: Filter results with this `<field_name>:<field_value>` (use `:` as a seaparator)",
)

### PAGINATION
page_number = Query(
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

per_page = Query(
  10, 
  alias="per_page",
  title="Results per page",
  description="`int`: Number of results per page",
)
sort_by = Query(
  None, 
  alias="sort_by",
  title="Sort by field",
  description="`str`: Field to sort by",
)

class OrderEnum(str, Enum) :
  asc = 'asc'
  desc = 'desc'

sort_order = Query(
  'asc', 
  alias="sort_order",
  title="Sort order field",
  description="`str`: Sort order for results",
)
shuffle_seed = Query(
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

version = Query(
  'last', 
  alias="version",
  title="Data version",
  description="`str`: version of the data requested",
)


class DataFormats(str, Enum) :
  json = 'json'
  geojson = 'geojson'

data_format = Query(
  'json', 
  alias="data_format",
  title="Data format",
  description="`str`: format results",
)

for_map = Query(
  False, 
  alias="for_map",
  title="For map",
  description="`bool`: format results for map",
)

normalize_data = Query(
  False, 
  alias="normalize_data",
  title="Normalize data",
  description="`bool`: fnormalize uploaded data",
)

field_to_return = Query(
  None, 
  alias="field_to_return",
  title="Field to return",
  description="`str`: Field to return",
)

fields_to_return = Query(
  None, 
  alias="fields_to_return",
  title="Fields to return",
  description="`str`: Fields to return. Separate the fields by a comma after the parameter : `&fields_to_return=<field_A>,<field_B>`",
)






### dependencies injection

async def query_parameters(
  q: list = query_str, 
  version: VersionsEnum = version,
  filter: list = search_filter, 
  ):
 return {
    "q" : q,
    "version" : version,
    "filter" : filter,
  }

async def version_parameters(
  version: VersionsEnum = version,
  ):
 return {
    "version" : version,
  }

async def pagination_parameters(
  page: int = page_number,
  per_page: PerPageEnum = per_page,
  sort_by: str = sort_by,  
  sort_order: OrderEnum = sort_order,   
  shuffle_seed: int = shuffle_seed,  
  ):
  return {
    "page" : page,
    "per_page" : per_page,
    "sort_by" : sort_by, 
    "sort_order" : sort_order, 
    "shuffle_seed" : shuffle_seed, 
  }

async def fields_parameters(
  field_to_return: list = field_to_return, 
  fields_to_return: str = fields_to_return,
  ):
  return {
    "field_to_return" : field_to_return,
    "fields_to_return" : fields_to_return,
  }

async def format_parameters(
  data_format : DataFormats = data_format,
  for_map: bool = for_map, 
  ):
  return {
    "data_format" : data_format,
    "for_map" : for_map,
  }

async def resp_parameters(
  only_data: bool = only_data,
  ):
  return {
    "only_data" : only_data,
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