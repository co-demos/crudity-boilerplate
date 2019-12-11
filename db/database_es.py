from log_config import log_, pformat

log_.debug(">>> db/database_es.py")

from datetime import datetime
from elasticsearch import Elasticsearch

from core.config import *

# from core.config import (
#   DB_ELASTICSEARCH,
#   ELASTICSEARCH_HOSTS,
#   ELASTICSEARCH_PORT,
#   ELASTICSEARCH_USER,
#   ELASTICSEARCH_PASSWORD,
#   ELASTICSEARCH_SCHEME
# )


log_.debug("DB_ELASTICSEARCH_MODE : %s", DB_ELASTICSEARCH_MODE)
log_.debug("ELASTICSEARCH_HOSTS_LOCAL : %s", ELASTICSEARCH_HOSTS_LOCAL)
log_.debug("ELASTICSEARCH_PORT_LOCAL : %s", ELASTICSEARCH_PORT_LOCAL)
log_.debug("ELASTICSEARCH_USER_LOCAL : %s", ELASTICSEARCH_USER_LOCAL)
log_.debug("ELASTICSEARCH_PASSWORD_LOCAL : %s", ELASTICSEARCH_PASSWORD_LOCAL)
log_.debug("ELASTICSEARCH_SCHEME_LOCAL : %s", ELASTICSEARCH_SCHEME_LOCAL)

if DB_ELASTICSEARCH_MODE and DB_ELASTICSEARCH_MODE != 'disabled' : 
  
  if DB_ELASTICSEARCH_MODE == 'local' : 
    es = Elasticsearch(
      ELASTICSEARCH_HOSTS_LOCAL,
      http_auth=(ELASTICSEARCH_USER_LOCAL, ELASTICSEARCH_PASSWORD_LOCAL),
      scheme=ELASTICSEARCH_SCHEME_LOCAL, # "https",
      port=ELASTICSEARCH_PORT_LOCAL,
    )

  if DB_ELASTICSEARCH_MODE == 'distant' : 
    es = Elasticsearch(
      ELASTICSEARCH_HOSTS,
      http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
      scheme=ELASTICSEARCH_SCHEME, # "https",
      port=ELASTICSEARCH_PORT,
    )

else : 
  es = None



