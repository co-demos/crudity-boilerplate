from log_config import log_, pformat
import inspect 

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

def check_index_check(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  ):
  """ check if index already exists.""" 

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

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


  status = { 'status_code' : 200 }
  res = {}


  log_.debug( "res : \n%s", pformat(res))
  return res, status



def create_index_check(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  index_params: dict = None,
  ):
  """ create an indeex if doesn't already exist"""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### check if index exists in ES
  is_index = check_index_check (
    index_name = index_name,
    doc_type = doc_type,
    doc_uuid = doc_uuid,
  )

  ### TO DO
  if ES_ENABLED :
    ### if doesn't exist, create it
    pass
    
  ### TO DO
  if MONGODB_ENABLED :
    ### check if index exists in MONGODB
    ### if doesn't exist, create it
    pass


  status = { 'status_code' : 200 }
  res = {}


  log_.debug( "res : \n%s", pformat(res))
  return res, status



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

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  # status = { 'status_code' : 200 }
  # res = {}

  if ES_ENABLED :
    res_es, status_es = view_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid
    )
    log_.debug( "res_es : \n%s", pformat(res_es))
    log_.debug( "status_es : \n%s", pformat(status_es))
    res, status = res_es, status_es


  if MONGODB_ENABLED :
    ### only view doc from MongoDB if `version!='last'` in query
    res_mongodb, status_mongodb = view_mongodb_document(
      database=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
    )


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def search_documents(
  index_name: str = None,
  doc_type: str = None,
  query_params: dict = None,
  ):
  """ search a document from ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }
  res = {}

  if ES_ENABLED :
    res_es, status_es = search_es_documents(
      index_name=index_name,
      doc_type=doc_type,
      query=query_params
    )
    log_.debug( "res_es : \n%s", pformat(res_es))
    log_.debug( "status_es : \n%s", pformat(status_es))
    res, status = res_es, status_es
    
  if MONGODB_ENABLED :
    ### only search docs from MongoDB if `version!='last'` in query
    res_mongodb, status_mongodb = search_mongodb_documents(
      database=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      query=query_params
    )


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def create_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  body = None,
  ):
  """ create a document in ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  if ES_ENABLED :
    res_es = add_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=body,
    )

  if MONGODB_ENABLED :
    res_mongodb = add_mongodb_document(
      database=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=body,
    )

  status = { 'status_code' : 200 }
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def create_version_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  version: int = None,
  body = None,
  ):
  """ create a version document in MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass

  status = { 'status_code' : 200 }
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def update_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  body = None,
  ):
  """ update a document in ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass


  status = { 'status_code' : 200 }
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def remove_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  ):
  """ remove a document from ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  if ES_ENABLED :
    res_es = remove_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
    )

  if MONGODB_ENABLED :
    pass


  status = { 'status_code' : 200 }
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status


def remove_many_document(
  index_name: str = None,
  doc_type: str = None,
  params: dict = None,
  ):
  """ remove a document from ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  if ES_ENABLED :
    pass
    
  if MONGODB_ENABLED :
    pass


  status = { 'status_code' : 200 }
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status