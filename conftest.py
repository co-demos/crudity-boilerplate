import pytest
from tests.utils.utils import client
from tests.api.api_v1.test_login import client_login, client_anonymous_login


@pytest.fixture
def client_ano_access_token() : 
  ano_user = client_anonymous_login( as_test=False, only_access_token=True )
  return ano_user 

@pytest.fixture
def client_access_token() : 
  user = client_login( as_test=False, only_access_token=True )
  return user 

@pytest.fixture
def user_headers() : 

  test_user_access_token = client_login( as_test = False, only_access_token=True )

  headers = {
    'accept': 'application/json',
    'access_token' : test_user_access_token,
  }

  return headers