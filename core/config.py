import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only

from utils.env import getenv_boolean

from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)

print ("... os.environ : ")
pp.pprint(os.environ.__dict__)


### APP SERVER CONFIG ENV
PROJECT_NAME = os.getenv("PROJECT_NAME")
PROJECT_VERSION = os.getenv("PROJECT_VERSION")
API_V1_STR = f"/api/{PROJECT_VERSION}"

AUTH_MODE = os.getenv("AUTH_MODE", "default")

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
  SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SENTRY_DSN = os.getenv("SENTRY_DSN")
SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv(
  "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://dev.couchbase-project.com, https://stag.couchbase-project.com, https://couchbase-project.com, http://local.dockertoolbox.tiangolo.com"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

DB_ELASTICSEARCH = os.getenv("DB_ELASTICSEARCH")
DB_MONGODB = os.getenv("DB_MONGODB")


### ELASTIC SEARCH CONFIG ENV
if DB_ELASTICSEARCH and DB_ELASTICSEARCH != 'disabled' : 

  ### local params
  ELASTICSEARCH_HOSTS_LOCAL = []
  es_hosts_local_raw = os.getenv("ELASTICSEARCH_HOSTS_LOCAL")
  if es_hosts_local_raw != None : 
    es_hosts = es_hosts_local_raw.split(",")
    for host in es_hosts:
      use_host = host.strip()
      ELASTICSEARCH_HOSTS_LOCAL.append(use_host)
    ELASTICSEARCH_PORT_LOCAL = os.getenv("ELASTICSEARCH_PORT_LOCAL")
    ELASTICSEARCH_USER_LOCAL = os.getenv("ELASTICSEARCH_USER_LOCAL")
    ELASTICSEARCH_PASSWORD_LOCAL = os.getenv("ELASTICSEARCH_PASSWORD_LOCAL")
    ELASTICSEARCH_SCHEME_LOCAL = os.getenv("ELASTICSEARCH_SCHEME_LOCAL")

  ### distant/prod params
  ELASTICSEARCH_HOSTS = []
  es_hosts_raw = os.getenv("ELASTICSEARCH_HOSTS")
  if es_hosts_raw != None : 
    es_hosts = es_hosts_raw.split(",")
    for host in es_hosts:
      use_host = host.strip()
      ELASTICSEARCH_HOSTS.append(use_host)
    ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT")
    ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER")
    ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
    ELASTICSEARCH_SCHEME = os.getenv("ELASTICSEARCH_SCHEME")


### MONGODB CONFIG ENV
if DB_MONGODB and DB_MONGODB != 'disabled' : 

  MONGO_ROOT_LOCAL=os.getenv("MONGO_ROOT_LOCAL")
  MONGO_PORT_LOCAL=os.getenv("MONGO_PORT_LOCAL")
  
  MONGO_ROOT_SERVER=os.getenv("MONGO_ROOT_SERVER")
  MONGO_PORT_SERVER=os.getenv("MONGO_PORT_SERVER")
  MONGO_USER_SERVER=os.getenv("MONGO_USER_SERVER")
  MONGO_PASS_SERVER=os.getenv("MONGO_PASS_SERVER")
  MONGO_OPTIONS_SERVER=os.getenv("MONGO_OPTIONS_SERVER")
  MONGO_DISTANT_URI=os.getenv("MONGO_DISTANT_URI")
  MONGO_DISTANT_URI_OPTIONS=os.getenv("MONGO_DISTANT_URI_OPTIONS")

  MONGO_DBNAME=os.getenv("MONGO_DBNAME")

  MONGO_COLL_USERS=os.getenv("MONGO_COLL_USERS")
  MONGO_COLL_DATASETS_INPUTS=os.getenv("MONGO_COLL_DATASETS_INPUTS")
  MONGO_COLL_DATASETS_RAWS=os.getenv("MONGO_COLL_DATASETS_RAWS")
  MONGO_COLL_DATAMODELS_FIELDS=os.getenv("MONGO_COLL_DATAMODELS_FIELDS")
  MONGO_COLL_DATAMODELS_TEMPLATES=os.getenv("MONGO_COLL_DATAMODELS_TEMPLATES")