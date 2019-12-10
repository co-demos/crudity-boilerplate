from enum import Enum, IntEnum
from pydantic import BaseModel

from fastapi import Query


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

for_map = Query(
  False, 
  alias="for_map",
  title="For map",
  description="`bool`: format results for map",
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