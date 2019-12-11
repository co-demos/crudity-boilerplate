from log_config import log_, pformat

log_.debug(">>> db/database_mongodb.py")

from core.config import *

from pymongo import MongoClient


log_.debug("DB_MONGODB_MODE : %s", DB_MONGODB_MODE)
