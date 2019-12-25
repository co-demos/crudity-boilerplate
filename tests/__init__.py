import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only


print ('loading : tests/__init__.py ... starting ')


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

print ('loading : tests/__init__.py ... finished ')