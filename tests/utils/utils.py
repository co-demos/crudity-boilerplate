import requests

from core import config


def get_server_api():
  server_name = f"http://{config.SERVER_NAME}"
  return server_name