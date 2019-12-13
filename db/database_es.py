from log_config import log_, pformat

print()
log_.debug(">>> db/database_es.py")

from datetime import datetime
from elasticsearch import Elasticsearch

from core.config import *

log_.debug("DB_ELASTICSEARCH_MODE : %s", DB_ELASTICSEARCH_MODE)
log_.debug("ELASTICSEARCH_HOSTS_LOCAL : %s", ELASTICSEARCH_HOSTS_LOCAL)
log_.debug("ELASTICSEARCH_PORT_LOCAL : %s", ELASTICSEARCH_PORT_LOCAL)
log_.debug("ELASTICSEARCH_USER_LOCAL : %s", ELASTICSEARCH_USER_LOCAL)
log_.debug("ELASTICSEARCH_PASSWORD_LOCAL : %s", ELASTICSEARCH_PASSWORD_LOCAL)
log_.debug("ELASTICSEARCH_SCHEME_LOCAL : %s", ELASTICSEARCH_SCHEME_LOCAL)


""" 
TUTORIALS Elastic Search :

cf : https://medium.com/the-andela-way/getting-started-with-elasticsearch-python-part-two-1c0c9d1117ea

"""

### ELASTIC SEARCH CLIENT

def create_es_client( 
  debug=False 
  ): 
  """Function to create an ES client."""

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


  if not es or not es.ping():
    log_.error("ES connection failed...")
    raise ValueError("ES connection failed")

  else :
    # print ( pformat( es.__dict__) )
    if debug :
      log_.debug("ES connection OK...")
    return es



### INDEX LEVEL

def create_es_index(
  es=create_es_client(),
  index_name=None
  ):
  """Functionality to create index."""

  res = es.indices.create(
    index=index_name
  )

  log_.debug( "res : \n%s", pformat(res))
  return res  


def delete_es_index(
  es=create_es_client(),
  index_name=None
  ):
  """Delete an index by specifying the index name"""
  
  res = es.indices.delete(
    index=index_name
  )
  
  log_.debug( "res : \n%s", pformat(res))
  return res  



### UTILS

def build_es_query( 
  query={}
  ):
  """Function to build a ES search query."""

  log_.debug( "query : \n%s", pformat(query))

  ### TO DO ...
  search_body = {
    'query':{
      'match':{
        "about": "play cricket"
      }
    }
  }

  return search_body



### DOCS LEVEL REQUESTS

def view_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None
  ):
  """Function to view a ES document."""

  res = es.get(
    index=index_name, 
    doc_type=doc_type, 
    id=doc_uuid
    )

  log_.debug( "res : \n%s", pformat(res))
  return res



def search_es_documents(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  query={}
  ):

  """Function to make a ES searrch query."""

  ### build search query
  search_body = build_es_query( query )

  res = es.search(
    index='megacorp',
    doc_type='employee',
    body=search_body
  )

  log_.debug( "res : \n%s", pformat(res))
  return res



def add_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  doc_body=None
  ):
  """
  Funtion to add an ES document by providing index_name,
  document type, document contents as doc and document id.
  """
  
  res = es.index(
    index=index_name,
    doc_type=doc_type,
    id=doc_uuid,
    body=doc_body
  )

  log_.debug( "res : \n%s", pformat(res))
  return res



def update_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  doc_body=None,
  new=None
  ):
  """Function to edit a document either updating existing fields or adding a new field."""

  if doc_body : 
    res = es.index(
      index=index_name,
      doc_type=doc_type,
      id=doc_uuid,
      body=doc_body
    )
  else : 
    res = es.update(
      index=index_name,
      doc_type=doc_type,
      id=doc_uuid,
      body={ "doc" : new }
    )

  log_.debug( "res : \n%s", pformat(res))
  return res



def remove_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None
  ):
  """Function to delete a specific document."""

  res = es.delete(
    index=index_name,
    doc_type=doc_type,
    id=doc_uuid
  )

  log_.debug( "res : \n%s", pformat(res))
  return res