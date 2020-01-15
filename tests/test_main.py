import pytest
from tests.utils.utils import get_server_api, client


@pytest.mark.server
def test_run_client_docs():
  response = client.get("/docs")
  assert response.status_code == 200