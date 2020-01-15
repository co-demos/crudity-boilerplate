import pytest

from log_config import log_, pformat

from core import config
from tests.utils.utils import get_server_api, client
from tests.api.api_v1.test_login import client_login

from tests.api.api_v1.test_dataset_inputs_endpoints import create_one_dsi, get_one_dsi, update_one_dsi, delete_one_dsi, delete_all_dsi
from tests.api.api_v1.test_dataset_raws_endpoints   import create_one_dsr, get_one_dsr, update_one_dsr, delete_one_dsr


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### TO DO - LOAD CSV FILES TO CRUDo
### - - - - - - - - - - - - - - - - - - - - - - - ### 

@pytest.mark.data
@pytest.mark.skip(reason='not developped yet')
def test_load_data_csv():
  pass


@pytest.mark.data
@pytest.mark.skip(reason='not developped yet')
def test_load_data_csv_bulk():
  pass