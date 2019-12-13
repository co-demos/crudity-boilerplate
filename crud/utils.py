from log_config import log_, pformat

import uuid
from core import config


print()
log_.debug(">>> crud/utils.py")

ES_ENABLED = config.DB_ELASTICSEARCH_MODE and config.DB_ELASTICSEARCH_MODE != 'disabled'
log_.debug(">>> ES_ENABLED : %s", ES_ENABLED)
if ES_ENABLED :
  from db.database_es import *

MONGODB_ENABLED = config.DB_MONGODB_MODE and config.DB_MONGODB_MODE != 'disabled'
log_.debug(">>> MONGODB_ENABLED : %s", MONGODB_ENABLED)
if MONGODB_ENABLED :
  from db.database_mongodb import *



### INDEX LEVEL

def create_index_check(
  index_name: str = None,
  doc_type: str = None,
  index_params: dict = None,
  ):

  ### TO DO
  if ES_ENABLED :
    ### check if index exists in ES
    ### if doesn't exist, create it
    pass
    
  ### TO DO
  if MONGODB_ENABLED :
    ### check if index exists in MONGODB
    ### if doesn't exist, create it
    pass


  res = {}


  log_.debug( "res : \n%s", pformat(res))
  return res



### UTILS

def generate_new_id():
  return str( uuid.uuid4() )



### GENERIC REQUESTS

def view_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  query_params: dict = None,
  ):
  """ get a document from ES / MongoDB """

  log_.debug( "query_params : \n%s", pformat(query_params))

  if ES_ENABLED :
    res = view_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid
    )
    
  if MONGODB_ENABLED :
    ### only view doc from MongoDB if `version!='last'` in query

    res = view_mongodb_document(
      database=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
    )

  res = {}


  log_.debug( "res : \n%s", pformat(res))
  return res



def search_documents(
  index_name: str = None,
  doc_type: str = None,
  query_params: dict = None,
  ):
  """ search a document from ES / MongoDB """

  res = {}

  if ES_ENABLED :
    res = search_es_documents(
      index_name=index_name,
      doc_type=doc_type,
      query=query_params
    )
    
  if MONGODB_ENABLED :
    ### only search docs from MongoDB if `version!='last'` in query
    res = search_mongodb_documents(
      database=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      query=query_params
    )


  log_.debug( "res : \n%s", pformat(res))
  return res



def create_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  body = None,
  ):
  """ create a document in ES / MongoDB """


  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass


  res = {}

  log_.debug( "res : \n%s", pformat(res))
  return res



def create_version_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  version: int = None,
  body = None,
  ):
  """ create a version document in MongoDB """

  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass

  res = {}

  log_.debug( "res : \n%s", pformat(res))
  return res



def update_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  body = None,
  ):
  """ update a document in ES / MongoDB """

  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass


  res = {}

  log_.debug( "res : \n%s", pformat(res))
  return res



def remove_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  ):
  """ remove a document from ES / MongoDB """


  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass


  res = {}

  log_.debug( "res : \n%s", pformat(res))
  return res


def remove_many_document(
  index_name: str = None,
  doc_type: str = None,
  params: dict = None,
  ):
  """ remove a document from ES / MongoDB """


  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass


  res = {}

  log_.debug( "res : \n%s", pformat(res))
  return res