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



es = Elasticsearch(
    ELASTICSEARCH_HOSTS,
    http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    scheme=ELASTICSEARCH_SCHEME, # "https",
    port=ELASTICSEARCH_PORT,
)

