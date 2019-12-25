from starlette.testclient import TestClient

from main import app

client = TestClient(app)


### cf : https://fastapi.tiangolo.com/tutorial/testing/

def test_run_client_docs():
  response = client.get("/docs")
  assert response.status_code == 200