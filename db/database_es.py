from log_config import log_, pformat
import inspect 

print()
log_.debug(">>> db/database_es.py")

from datetime import datetime
from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch_dsl import Search

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
    print()
    raise ValueError("ES connection failed")

  else :
    # print ( pformat( es.__dict__) )
    if debug :
      log_.debug("ES connection OK...")
      print()
    return es



### INDEX LEVEL

def check_es_index(
  es=create_es_client(),
  index_name=None,
  ):
  """Functionality to check if index exists."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }

  try :
    res = es.indices.exists(index=index_name)
  except ElasticsearchException as err :
    res = None
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status


def create_es_index(
  es=create_es_client(),
  index_name=None,
  is_update=False
  ):
  """Functionality to create index."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }

  try : 
    if is_update == False :
      # cf : https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.create
      res = es.indices.create(
        index=index_name
      )
    else : 
      # cf : https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.client.IndicesClient.upgrade
      res = es.indices.upgrade(
        index=index_name
      )
  except ElasticsearchException as err :
    res = None
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status


def delete_es_index(
  es=create_es_client(),
  index_name=None
  ):
  """Delete an index by specifying the index name"""
  
  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }

  try :
    res = es.indices.delete(
      index=index_name
    )
  except ElasticsearchException as err :
    res = None
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }
  
  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



### UTILS

def build_es_query( 
  query={}
  ):
  """Function to build a ES search query."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### query parts
  matchs = {}
  filters = {}

  ### TO DO ...
  search_body = {

    'query': {

      # 'match_all': {
      # },
      # 'match': {
        # "author": {
        #   "query": "Victor Hugo",
        #   "operator": "and" 
        # },
      # },
      # "match_phrase": {
        # "author": "Victor Hugo"
      # },
      # "match_phrase_prefix": { 
        # "author": "Victor Hu"
      # },
      # "multi_match" : {
        # "query" : "Victor Hugo",
        # "fields" : [ "author", "description" ]
      # },
      # 'query_string': {
        # "fields": ["content","title^2","author.*"],
        # "query": "Victor AND Hugo OR 1862"
      # },
      # "simple_query_string": {
        # "fields": ["content","title^2","author.*"],
        # "query": "Victor AND Hugo OR 1862" 
      # },


      # "exists": {
        # "field": "subtitles"
      # },
      # "type": {
        # "value": "books"
      # },
      # "term": {
        # "lang": "fr",
        # "_type": "book"
      # },
      # "prefix": {
        # "content": "rom" 
      # },
      # "wildcard": {
        # "title": "du?l*"
      # },
      # "ids" : {
        # "type" : "book",
        # "values" : ["4", "12", "38"] 
      # },


      # "range" : { 
        # "price" : {
        #   "gte" : 50,
        #   "lt" : 200 
        # },
        # "created": {
        #   "gte" : "2015-12-15"
        # },
        # "created": {
        #   "gte" : "now-1d/d", 
        #   "lt" : "now/d" 
        #   "relation" : "within" # 'within', 'contains' or 'intersects'(default)
        # },
      # },


      # "fuzzy": {
        # "author": {
        #   "value": "vitcor", "fuzziness": 2, "prefix_length": 1
        # }
      # },


      # "bool": {
        # "must": [
        #   {"match": {"title": "spring in action" }}, { "term": { "tag": "spring" }}
        # ],
        # "must_not": { 
          # "range": {"year": { "lte": 2010 } },
          # "exists": { "field": "user" }
        # },
        # "should": [
        #   {"term": { "tag": "java" }},
        #   {"term": { "categories": "development" }},
        # ],
        # "filter": {
          # "range": { "price": {"gt": 25, "lt": 50} 
        # }
      # },

    },

    'aggs' : {

    },

    'sort' : {
      # { "title.keyword" : "desc" },
      # { "price" : {"order" : "asc", "missing" : "_last"} }, 
      # { "category" : {"unmapped_type" : "string"} }, "_score"]
    }

  }

  # return search_body
  return {}



### DOCS LEVEL REQUESTS

def view_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None
  ):
  """Function to view a ES document."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }

  try : 
    res = es.get(
      index=index_name, 
      doc_type=doc_type, 
      id=doc_uuid
    )
  except ElasticsearchException as err : 
    res = None
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def search_es_documents(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  query={}
  ):

  """Function to make a ES searrch query."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }
  res = None

  ### build search query
  search_body = build_es_query( query )
  log_.debug( "search_body : \n%s", pformat(search_body))
  

  try : 
    
    # s = Search(using=es, index=index_name) \
    #     .filter( "term", category="search") \
    #     .query( "match", title="python")   \
    #     .exclude( "match", description="beta")

    res = es.search(
      index=index_name,
      # doc_type=doc_type,
      body=search_body
    )
    res = res['hits']['hits']

  except ElasticsearchException as err : 
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



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
  
  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }
  res = None

  try : 
    # pass
    res = es.index(
      index=index_name,
      doc_type=doc_type,
      id=doc_uuid,
      body=doc_body
    )
  except ElasticsearchException as err : 
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def update_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None,
  doc_body=None,
  new=None
  ):
  """Function to edit a document either updating existing fields or adding a new field."""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }

  if doc_body : 
    try :
      res = es.index(
        index=index_name,
        doc_type=doc_type,
        id=doc_uuid,
        body=doc_body
      )
    except ElasticsearchException as err : 
      res = None
      status = {
        'status_code' : err.status_code,
        'error' : err.error,
        'info' : err.info,
      }

  else : 
    try : 
      res = es.update(
        index=index_name,
        doc_type=doc_type,
        id=doc_uuid,
        body={ "doc" : new }
      )
    except ElasticsearchException as err : 
      res = None
      status = {
        'status_code' : err.status_code,
        'error' : err.error,
        'info' : err.info,
      }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def remove_es_document(
  es=create_es_client(),
  index_name=None,
  doc_type=None,
  doc_uuid=None
  ):
  """Function to delete a specific document."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  try : 
    res = es.delete(
      index=index_name,
      doc_type=doc_type,
      id=doc_uuid
    )
  except ElasticsearchException as err : 
    res = None
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status


def remove_es_index(
  es=create_es_client(),
  index_name=None,
  ):
  """Function to delete a specific ES index."""

  status = { 'status_code' : 200 }

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  try : 
    res = es.delete(
      index=index_name,
    )
  except ElasticsearchException as err : 
    res = None
    status = {
      'status_code' : err.status_code,
      'error' : err.error,
      'info' : err.info,
    }

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status