import os

from dotenv import load_dotenv
from pathlib import Path  # python3 only

from utils.env import getenv_boolean

print("--- core/config.py ...")


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

def formatEnvVar(var_name, format_type='boolean', separator=',', dict_separator=":") : 

  # print("formatEnvVar / var_name : ", var_name)

  env_var = os.getenv(var_name)
  # print("formatEnvVar / env_var : {} / var_name : {} ".format(env_var, var_name) )

  # if format_type in ['boolean', 'string'] :
  if format_type in ['boolean'] :
    if env_var in [ 'y', 'Y','yes', 'Yes', 'YES', 'true', 'True', 'TRUE', '1'] : 
      return True
    else :
      return False

  # print("...")  

  # transform as none if it is the case
  if env_var in [ 'n', 'N', 'none', 'None', 'NONE', 'nan', 'Nan', 'NAN', 'null', 'Null','NULL', 'undefined'] : 
    env_var = None 
    if format_type == 'string' : 
      env_var = ""
    return env_var

  elif env_var and format_type == 'integer' : 
    return int(env_var)

  elif env_var and format_type == 'float' : 
    return float(env_var)

  elif env_var and format_type == 'list' : 
    return env_var.split(separator)

  elif env_var and format_type == 'dict' : 

    temp_list = env_var.split(separator)
    # print("formatEnvVar / temp_list : ", temp_list)
    env_dict = {}
    if len(temp_list) > 0 : 
      for tuple_dict in temp_list : 
        i = tuple_dict.split(dict_separator)
        env_dict[ i[0] ] = i[1] 
    return env_dict

  else : 
    return env_var


### APP SERVER CONFIG ENV
PROJECT_NAME = os.getenv("PROJECT_NAME")
PROJECT_VERSION = os.getenv("PROJECT_VERSION")
PROJECT_REPO = os.getenv("PROJECT_REPO")

ROLE_SUPERUSER = "superuser"

# API_V1_STR = f"/api/{PROJECT_VERSION}"
API_V1_STR = f"/api/v1"

APP_MODE = os.getenv("APP_MODE", "default")
AUTH_MODE = os.getenv("AUTH_MODE", "default")

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
  SECRET_KEY = os.urandom(32)

API_KEY = os.getenv("API_KEY", "1234567asdfgh")
# API_KEY_QUERY = os.getenv("API_KEY_QUERY", "access_token")
API_KEY_NAME = os.getenv("API_KEY_NAME", "access_token")
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "crudity.me")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SENTRY_DSN = os.getenv("SENTRY_DSN")
SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv(
  "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://dev.couchbase-project.com, https://stag.couchbase-project.com, https://couchbase-project.com, http://local.dockertoolbox.tiangolo.com"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days


### DB MODES
DB_ELASTICSEARCH_MODE = os.getenv("DB_ELASTICSEARCH_MODE", 'local')
DB_MONGODB_MODE = os.getenv("DB_MONGODB_MODE", 'local')


### ELASTIC SEARCH CONFIG ENV
if DB_ELASTICSEARCH_MODE and DB_ELASTICSEARCH_MODE != 'disabled' : 

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
if DB_MONGODB_MODE and DB_MONGODB_MODE != 'disabled' : 

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

  MONGO_BUILT_URI=None

### LOGS CONFIG
# LOGS_FOLDER=os.getenv("LOGS_FOLDER", '_logs')
# LOGS_FILE_INFOS=os.getenv("LOGS_FILE_INFOS", 'infos_logs.log')
# LOGS_FILE_WARNINGS=os.getenv("LOGS_FILE_WARNINGS", "warning_logs.log")
# LOGS_FILE_ERRORS=os.getenv("LOGS_FILE_ERRORS", "error_logs.log")




""" AUTH MODE """
AUTH_MODE = os.getenv("AUTH_MODE")

if AUTH_MODE != 'internal' :

  AUTH_URL_ROOT_LOCAL = os.getenv("AUTH_URL_ROOT_LOCAL")
  AUTH_URL_ROOT_DISTANT_PROD = os.getenv("AUTH_URL_ROOT_DISTANT_PROD")
  AUTH_URL_ROOT_DISTANT_PREPOD = os.getenv("AUTH_URL_ROOT_DISTANT_PREPOD")

  AUTH_URL_HEADERS = formatEnvVar('AUTH_URL_HEADERS', format_type='dict')
  AUTH_URL_HEADERS_PAYLOAD = formatEnvVar('AUTH_URL_HEADERS_PAYLOAD', format_type='dict')
  AUTH_URL_TOKEN_LOCATION = formatEnvVar('AUTH_URL_TOKEN_LOCATION', format_type='list')
  AUTH_URL_TOKEN_HEADER_NAME = os.getenv('AUTH_URL_TOKEN_HEADER_NAME')
  AUTH_URL_TOKEN_HEADER_TYPE = formatEnvVar('AUTH_URL_TOKEN_HEADER_TYPE', format_type='string')

  AUTH_URL_TOKEN_QUERY_STRING_NAME = os.getenv('AUTH_URL_TOKEN_QUERY_STRING_NAME', 'token')

  AUTH_DISTANT_ENDPOINTS = {
    
    ### LISTING USERS
    "users_list" : {
      "get_one" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_GET_ONE"),
        "method" :      os.getenv("AUTH_DISTANT_USER_GET_ONE_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_GET_ONE_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_GET_ONE_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_GET_ONE_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_GET_ONE_RESP', format_type='dict'),
      },
      "get_list"    : {
        "url" :         os.getenv("AUTH_DISTANT_USER_GET_LIST"),
        "method" :      os.getenv("AUTH_DISTANT_USER_GET_LIST_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_GET_LIST_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_GET_LIST_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_GET_LIST_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_GET_LIST_RESP', format_type='dict'),
      },
    },

    ### EDIT USER
    "user_edit" : {
      "register" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_REGISTER"),
        "method" :      os.getenv("AUTH_DISTANT_USER_REGISTER_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_REGISTER_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_REGISTER_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_REGISTER_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_REGISTER_RESP', format_type='dict'),
      },
      "confirm_email" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_CONF_EMAIL"),
        "method" :      os.getenv("AUTH_DISTANT_USER_CONF_EMAIL_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_RESP', format_type='dict'),
      },
      "user_update" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_EDIT"),
        "method" :      os.getenv("AUTH_DISTANT_USER_EDIT_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_EDIT_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_EDIT_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_EDIT_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_EDIT_RESP', format_type='dict'),
      },
      "user_delete" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_DELETE"),
        "method" :      os.getenv("AUTH_DISTANT_USER_DELETE_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_DELETE_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_DELETE_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_DELETE_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_DELETE_RESP', format_type='dict'),
      },
    },
    ###
    "user_login" : {
      "login" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_LOGIN"),
        "method" :      os.getenv("AUTH_DISTANT_USER_LOGIN_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_LOGIN_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_LOGIN_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_RESP', format_type='dict'),
      },
      "login_anonymous" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_LOGIN_ANO"),
        "method" :      os.getenv("AUTH_DISTANT_USER_LOGIN_ANO_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_RESP', format_type='dict'),
      },
    },
    ###
    "auth_tokens" : {
      "confirm_access" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_TOK_CONFIRM"),
        "method" :      os.getenv("AUTH_DISTANT_USER_TOK_CONFIRM_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_RESP', format_type='dict'),
      },
      "fresh_access_token" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_TOK_FRESH"),
        "method" :      os.getenv("AUTH_DISTANT_USER_TOK_FRESH_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_RESP', format_type='dict'),
      },
      "new_access_token" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_TOK_NEW"),
        "method" :      os.getenv("AUTH_DISTANT_USER_TOK_NEW_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_RESP', format_type='dict'),
      },
      "new_refresh_token" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_TOK_NEW_REFRESH"),
        "method" :      os.getenv("AUTH_DISTANT_USER_TOK_NEW_REFRESH_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_RESP', format_type='dict'),
      },
      "token_claims" : {
        "url" :         os.getenv("AUTH_DISTANT_USER_TOK_CLAIMS"),
        "method" :      os.getenv("AUTH_DISTANT_USER_TOK_CLAIMS_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_POST_ARGS', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_URL_APPEND', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_RESP', format_type='dict'),
      },
    },
    ###
    "auth_password" : {
      "pwd_forgot" : {
        "url" :         os.getenv("AUTH_DISTANT_PWD_FORGOT"),
        "method" :      os.getenv("AUTH_DISTANT_PWD_FORGOT_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_PWD_FORGOT_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_PWD_FORGOT_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_PWD_FORGOT_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_PWD_FORGOT_RESP', format_type='dict'),
      },
      "pwd_reset" : {
        "url" :         os.getenv("AUTH_DISTANT_PWD_RESET"),
        "method" :      os.getenv("AUTH_DISTANT_PWD_RESET_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_PWD_RESET_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_PWD_RESET_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_RESP', format_type='dict'),
      },
      "pwd_reset_link" : {
        "url" :         os.getenv("AUTH_DISTANT_PWD_RESET_LINK"),
        "method" :      os.getenv("AUTH_DISTANT_PWD_RESET_LINK_METHOD"),
        "url_args" :    formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_URL_ARGS', format_type='dict'),
        "url_append" :  formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_URL_APPEND', format_type='list'),
        "post_args" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_POST_ARGS', format_type='dict'),
        "resp_path" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_RESP', format_type='dict'),
      },
    }
  }