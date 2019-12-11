
import os
import click 

from dotenv import load_dotenv
from pathlib import Path  # python3 only

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from utils.env import get_boolean, getenv_boolean


from pprint import pprint, pformat, PrettyPrinter
pp = PrettyPrinter(indent=4)

### READ ENV VARS FROM HIDDEN .ENV FILES
env_path_global = Path('.') / 'env-backend.env'
load_dotenv(env_path_global, verbose=True)

# for ES
db_es_enabled = getenv_boolean("DB_ELASTICSEARCH_ENABLED")
if db_es_enabled : 
  env_path_elasticsearch = Path('.') / 'env-elasticsearch.env'
  load_dotenv(env_path_elasticsearch, verbose=True)

# for mongoDB
db_mongo_enabled = getenv_boolean("DB_MONGODB_ENABLED")
if db_mongo_enabled : 
  env_path_mongodb = Path('.') / 'env-mongodb.env'
  load_dotenv(env_path_mongodb, verbose=True)

# load config
from core import config

### LOAD ROUTER
from api.api_v1.api import api_router

app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")



### CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
  origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
  for origin in origins_raw:
    use_origin = origin.strip()
    origins.append(use_origin)
  app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  ),

app.include_router(api_router, prefix=config.API_V1_STR)



### READ ENV VARS FROM HIDDEN FILE
env_path_global = Path('.') / 'env-backend.env'
load_dotenv(env_path_global, verbose=True)


### APP RUNNER
@click.command()
@click.option('--mode',     default="default",     nargs=1,  help="The <mode> you need to run the app : default | testing | preprod | production" )
@click.option('--auth',     default="default",     nargs=1,  help="The <auth> mode you need to run the app : default | default_docker | server | server_docker | distant_preprod | distant_prod" )
@click.option('--host',     default="localhost",   nargs=1,  help="The <host> name you want the app to run on : <IP_NUMBER> " )
@click.option('--port',     default="8000",        nargs=1,  help="The <port> number you want the app to run on : <PORT_NUMBER>")
@click.option('--docker',   default="docker_off",  nargs=1,  help="Are you running the app with <docker> : docker_off | docker_on" )
@click.option('--mongodb',  default="local",       nargs=1,  help="The <mongodb> you need to run the app : disabled | local | distant | server" )
@click.option('--esdb',     default="local",       nargs=1,  help="The <esdb> you need to run the app : disabled | local | distant | server" )
@click.option('--https',    default="false",       nargs=1,  help="The <https> mode you want the app to run on : true | false")
def app_runner(mode, docker, mongodb, esdb, auth, host, port, https) :
  """
  app_runner

  """

  print ("= "*50)
  print ("= = = RERUN FLASK APP FROM APP RUNNER = = =")
  print ("= "*50)

  ### WARNING : CLIck will treat every input as string as defaults values are string too
  print ("\n=== CUSTOM CONFIG FROM CLI ===\n")
  print ("=== mode    : ", mode)
  print ("=== host    : ", host)
  print ("=== port    : ", port)
  print ("=== auth    : ", auth)
  # print ("=== docker  : ", docker)
  print ("=== mongodb : ", mongodb)
  print ("=== esdb    : ", esdb)
  # print ("=== https   : ", https)

  ### OVERRIDE ENV VARS FROM CLI 
  os.environ["APP_MODE"]      = mode
  os.environ["AUTH_MODE"]     = auth

  os.environ["SERVER_NAME"]   = host
  os.environ["SERVER_HOST"]   = port

  # os.environ["DOCKER_MODE"]   = docker

  os.environ["DB_ELASTICSEARCH"] = mongodb # get_boolean(mongodb)
  os.environ["DB_MONGODB"]       = esdb # get_boolean(esdb)

  pp.pprint(config.__dict__)

  uvicorn.run(app, host=host, port=int(port) )


if __name__ == "__main__":

  # pp.pprint(config.__dict__)
  # print ("... os.environ : ")
  # pp.pprint(os.environ)

  app_runner()