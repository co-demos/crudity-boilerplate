from log_config import log_, pformat
import inspect 

from models.dataset_input import *
from models.dataset_raw import *

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

def check_index(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  ):
  """ check if index already exists.""" 

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  is_index = False
  status = { 'status_code' : 200 }


  if ES_ENABLED :
    ### check if index exists in ES
    is_es_index, status_es = check_es_index (
      index_name = index_name,
    )
    is_index, status = is_es_index, status_es
  

  ### TO DO
  if MONGODB_ENABLED :
    ### check if index exists in MONGODB
    pass



  log_.debug( "is_index : %s", is_index )
  return is_index, status



def create_index_check(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  index_params: dict = None,
  ):
  """ create an index if doesn't already exist"""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### check if index exists in ES
  is_index, status_index = check_index (
    index_name = index_name,
    doc_type = doc_type,
    doc_uuid = doc_uuid,
  )

  status = { 'status_code' : 200 }
  res = {}

  
  ### TO DO
  if ES_ENABLED :
    ### if doesn't exist, create it
    pass
    
  ### TO DO
  if MONGODB_ENABLED :
    ### check if index exists in MONGODB
    ### if doesn't exist, create it
    pass




  log_.debug( "res : \n%s", pformat(res))
  return res, status



def update_index_check(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  index_params: dict = None,
  ):
  """ update an index if doesn't already exist"""

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  ### check if index exists in ES
  is_index = check_index (
    index_name = index_name,
    doc_type = doc_type,
    doc_uuid = doc_uuid,
  )

  status = { 'status_code' : 200 }
  res = {}

  
  ### TO DO
  if ES_ENABLED :
    ### if doesn't exist, create it
    pass
    
  ### TO DO
  if MONGODB_ENABLED :
    ### check if index exists in MONGODB
    ### if doesn't exist, create it
    pass




  log_.debug( "res : \n%s", pformat(res))
  return res, status




### UTILS

def generate_new_id( format = 'hex' ):

  ### cf : https://www.geeksforgeeks.org/generating-random-ids-using-uuid-python/ 
  
  new_id = uuid.uuid4()

  if format == 'hex' :
    new_id = new_id.hex
  elif format == 'int' : 
    new_id = new_id.int
  elif format == 'normal' : 
    new_id = str(new_id)
  else :
    new_id = str(new_id)

  return new_id



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

  status = { 'status_code' : 200 }
  res = {}

  q_version = query_params['version']

  if ES_ENABLED and q_version == 'last':
    res_es, status_es = view_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid
    )
    log_.debug( "res_es : \n%s", pformat(res_es))
    log_.debug( "status_es : \n%s", pformat(status_es))
    res, status = res_es, status_es


  if MONGODB_ENABLED and q_version != 'last' :
    ### only view doc from MongoDB if `version!='last'` in query
    res_mongodb, status_mongodb = view_mongodb_document(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
    )
    log_.debug( "res_mongodb : \n%s", pformat(res_mongodb))
    log_.debug( "status_mongodb : \n%s", pformat(status_mongodb))
    res, status = res_mongodb, status_mongodb

  # log_.debug( "res : \n%s", pformat(res))
  # print()
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

  q_version = query_params['version']

  if ES_ENABLED and q_version == 'last':
    res_es, status_es = search_es_documents(
      index_name=index_name,
      doc_type=doc_type,
      query=query_params,
    )
    # log_.debug( "res_es : \n%s", pformat(res_es))
    # log_.debug( "status_es : \n%s", pformat(status_es))
    res, status = res_es, status_es
    
  if MONGODB_ENABLED and q_version != 'last' :
    ### only search docs from MongoDB if `version!='last'` in query
    res_mongodb, status_mongodb = search_mongodb_documents(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      query=query_params
    )
    log_.debug( "res_mongodb : \n%s", pformat(res_mongodb))
    log_.debug( "status_mongodb : \n%s", pformat(status_mongodb))
    res, status = res_mongodb, status_mongodb

  # log_.debug( "res : \n%s", pformat(res))
  # print()
  return res, status



def create_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  body = None,
  ):
  """ create a document in ES / MongoDB """

  # log_.debug( "function : %s", inspect.stack()[0][3] )
  # log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }
  res = {}

  if ES_ENABLED :
    res_es, status_es = add_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=body,
    )
    log_.debug( "res_es : \n%s", pformat(res_es))
    log_.debug( "status_es : \n%s", pformat(status_es))
    res, status = res_es, status_es
    
  if MONGODB_ENABLED :
    body["version"] = 1
    body["_id"] = doc_uuid
    res_mongodb, status_mongodb = add_mongodb_document(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=body,
    )
    log_.debug( "res_mongodb : \n%s", pformat(res_mongodb))
    log_.debug( "status_mongodb : \n%s", pformat(status_mongodb))

  # log_.debug( "res : \n%s", pformat(res))
  # print()
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
    body["version"] = version
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

  full_update = params.get('full_update' , False) 


  if ES_ENABLED :

    ### get original doc
    orig_res_es, orig_status_es = view_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid
    )
    log_.debug( "orig_res_es : \n%s", pformat(orig_res_es))
    log_.debug( "orig_status_es : \n%s", pformat(orig_status_es))


    ### TO DO 
    ### compare original with doc_body
    # doc_body = body 
    # doc_body_dict = body.update_data
    doc_body_dict = body


    ### update doc in ES
    res_es, status_es = update_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=doc_body_dict,
      full_update = full_update 
    )

    res = res_es
    # status = { 'status_code' : status_es['status_code'] }
    status = status_es


  ### update doc in MongoDB
  if MONGODB_ENABLED :
    res_mongodb, status_mongodb = update_mongodb_document(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=doc_body_dict,
      full_update = full_update 
    )
    if ES_ENABLED == False :
      res = res_mongodb
      # status = { 'status_code' : status_mongodb['status_code'] }
      status = status_mongodb


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



# doc_uuid_list: List[str] = None,
def update_many_document(
  index_name: str = None,
  doc_type: str = None,
  params: dict = None,
  body = None,
  ):
  """ update many document in ES / MongoDB """

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

  status = { 'status_code' : 200 }
  res = {}

  if ES_ENABLED :
    res_es, status_es = remove_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
    )
    log_.debug( "res_es : \n%s", pformat(res_es))
    log_.debug( "status_es : \n%s", pformat(status_es))
    res, status = res_es, status_es

  if MONGODB_ENABLED :
    res_mongodb, status_mongodb = remove_mongodb_document(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
    )
    log_.debug( "res_mongodb : \n%s", pformat(res_mongodb))
    log_.debug( "status_mongodb : \n%s", pformat(status_mongodb))

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



def remove_many_documents(
  index_name: str = None,
  doc_type: str = None,
  params: dict = None,
  ):
  """ remove a document from ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  if ES_ENABLED :
    res_es, status_es = remove_es_index(
      index_name=index_name,
      doc_type=doc_type,
    )

  if MONGODB_ENABLED :
    res_mongodb, status_mongodb = remove_mongodb_many_documents(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
    )

  status = { 'status_code' : 200 }
  res = {}

  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status