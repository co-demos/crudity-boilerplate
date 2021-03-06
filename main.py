
print()
restart_str = "RESTARTING"
start_str_len = len(restart_str)
restart_symbol_1 = "/\_"
restart_symbol_2 = "\/‾"
start_symbol_len = len(restart_symbol_1)
start_multiplyer = 40  

print(restart_symbol_1*start_multiplyer)
print(" "*(start_symbol_len)*( round(start_multiplyer/2) - (round(start_str_len/start_symbol_len))), restart_str)
print(restart_symbol_2*start_multiplyer)

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

env_path_auth = Path('.') / 'env-auth.env'
load_dotenv(env_path_auth, verbose=True)

# for ES
# db_es_enabled = getenv_boolean("DB_ELASTICSEARCH_MODE")
db_es_enabled = os.getenv("DB_ELASTICSEARCH_MODE", 'disabled') != 'disabled'
if db_es_enabled : 
  env_path_elasticsearch = Path('.') / 'env-elasticsearch.env'
  load_dotenv(env_path_elasticsearch, verbose=True)

# for mongoDB
# db_mongo_enabled = getenv_boolean("DB_MONGODB_MODE")
db_mongo_enabled = os.getenv("DB_MONGODB_MODE", 'disabled') != 'disabled'
if db_mongo_enabled : 
  env_path_mongodb = Path('.') / 'env-mongodb.env'
  load_dotenv(env_path_mongodb, verbose=True)

# load config
from core import config

from log_config import log_, pformat
log_.debug( "... starting to log stuff ..." )


### LOAD ROUTER
from api.api_v1.api import api_router

app = FastAPI(
  title=config.PROJECT_NAME, 
  description=f"A <a href='{config.PROJECT_REPO}' target='_blank'>CRUDity</a> instance to expose your open data",
  version=config.PROJECT_VERSION,
  openapi_url="/api/v1/openapi.json"
  )



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

app.include_router(
  api_router, 
  prefix=config.API_V1_STR
)



default_mode    = config.APP_MODE
default_autoreload = config.APP_AUTORELOAD

default_auth    = config.AUTH_MODE

default_host    = config.SERVER_HOST
default_port    = config.SERVER_PORT

default_esdb    = config.DB_ELASTICSEARCH_MODE
default_mongodb = config.DB_MONGODB_MODE

default_docker  = 'docker_off'
default_https   = 'false'



### APP RUNNER
@click.command()
# @click.option('--mode',     default="default",     nargs=1,  help="The <mode> you need to run the app : default | testing | preprod | production" )
# @click.option('--auth',     default="default",     nargs=1,  help="The <auth> mode you need to run the app : no_auth | dev | default | default_docker | server | server_docker | distant_preprod | distant_prod" )
# @click.option('--host',     default="localhost",   nargs=1,  help="The <host> name you want the app to run on : <IP_NUMBER> " )
# @click.option('--port',     default="8000",        nargs=1,  help="The <port> number you want the app to run on : <PORT_NUMBER>")
# @click.option('--esdb',     default="local",       nargs=1,  help="The <esdb> you need to run the app : disabled | local | distant | server" )
# @click.option('--mongodb',  default="local",       nargs=1,  help="The <mongodb> you need to run the app : disabled | local | distant | server" )
# @click.option('--docker',   default="docker_off",  nargs=1,  help="Are you running the app with <docker> : docker_off | docker_on" )
# @click.option('--https',    default="false",       nargs=1,  help="The <https> mode you want the app to run on : true | false")
# @click.option('--reload_mode', default="true",         nargs=1,  help="The <https> mode you want the app to run on : true | false")
@click.option('--mode',       default=default_mode,       nargs=1,  help="The <mode> you need to run the app : default | dev | testing | preprod | production" )
@click.option('--autoreload', default=default_autoreload, nargs=1,  help="The <autoreload> mode you want the app to run on : true | false")
@click.option('--auth',     default=default_auth,         nargs=1,  help="The <auth> mode you need to run the app : no_auth | dev | default | default_docker | server | server_docker | distant_preprod | distant_prod" )
@click.option('--host',     default=default_host,         nargs=1,  help="The <host> name you want the app to run on : <IP_NUMBER> " )
@click.option('--port',     default=default_port,         nargs=1,  help="The <port> number you want the app to run on : <PORT_NUMBER>")
@click.option('--esdb',     default=default_esdb,         nargs=1,  help="The <esdb> you need to run the app : disabled | local | distant | server" )
@click.option('--mongodb',  default=default_mongodb, nargs=1,  help="The <mongodb> you need to run the app : disabled | local | distant | server" )
@click.option('--docker',   default=default_docker,  nargs=1,  help="Are you running the app with <docker> : docker_off | docker_on" )
@click.option('--https',    default="false",         nargs=1,  help="The <https> mode you want the app to run on : true | false")
def app_runner(mode, auth, host, port, esdb, mongodb, docker, https, autoreload) :
  """
  app_runner

  """

  print ("= "*50)
  print ("= = = RERUN FLASK APP FROM APP RUNNER = = =")
  print ("= "*50)

  ### WARNING : CLIck will treat every input as string as defaults values are string too
  print ("\n=== CUSTOM CONFIG FROM CLI ===\n")
  print ("=== mode    : ", mode)
  print ("=== autoreload  : ", autoreload)
  print ("=== host    : ", host)
  print ("=== port    : ", port)
  print ("=== auth    : ", auth)
  print ("=== mongodb : ", mongodb)
  print ("=== esdb    : ", esdb)

  print ("=== https   : ", https)
  print ("=== docker  : ", docker)

  ### OVERRIDE ENV VARS FROM CLI 
  os.environ["APP_MODE"]      = mode
  os.environ["AUTH_MODE"]     = auth

  os.environ["SERVER_HOST"]   = host
  os.environ["SERVER_PORT"]   = port

  cli_server_name = f"{host}:{port}"
  if config.SERVER_NAME != cli_server_name :
    os.environ["SERVER_NAME"] = cli_server_name

  os.environ["DB_ELASTICSEARCH"] = esdb # get_boolean(mongodb)
  os.environ["DB_MONGODB"]       = mongodb  # get_boolean(esdb)

  os.environ["DOCKER_MODE"]   = docker

  print ("\n=== config : \n")
  pp.pprint(config.__dict__)





  reload_string = ""
  autoreload_bool = False
  if autoreload in [ True, 'y', 'Y','yes', 'Yes', 'YES', 'true', 'True', 'TRUE', '1'] : 
    autoreload_bool = True
    os.environ["APP_AUTORELOAD"] = "True"
    reload_string = "--reload"

  # uvicorn.run(
  #   app, 
  #   host=host, 
  #   port=int(port), 
  #   # reload=autoreload_bool     ### not working programmatically
  # )

  os.system( f"uvicorn main:app {reload_string} --host={host} --port={port}" )



if __name__ == "__main__":

  log_.debug( "... starting __name__ == '__main__' ..." )

  app_runner()