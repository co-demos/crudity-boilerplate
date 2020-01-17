from log_config import log_, pformat
import inspect 

from models.auth import *
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


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### AUTH LEVEL
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def is_user_authorized( 
  user: dict = {},
  doc_auth: DocAuthData = DocAuthData(),
  level = 'read'
  ):

  # level: str = None

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))


  ### user auth data
  user_infos = user.get('infos', None) 
  user_email = user_infos.get('email', 'no_email')

  user_auth  = user.get('auth', None) 
  user_role  = user_auth.get('role', None) 

  ### doc auth data
  log_.debug( "doc_auth.dict() : \n%s", pformat(doc_auth.dict()))

  doc_owner         = doc_auth.owner
  doc_team          = doc_auth.team
  doc_auth_preview  = doc_auth.auth_preview
  doc_auth_modif    = doc_auth.auth_modif

  ### check if user is the doc's owner / creator
  is_user_owner     = user_email == doc_owner


  ### check if user is authorized as team member
  is_user_authorized_in_team = False
  user_from_team = { 'roles' : None }

  if is_user_owner == False :
    
    # cf : https://workingninja.com/check-if-value-exists-list-dictionaries
    is_user_in_team = any( team_member.get('email') == user_email for team_member in doc_team )

    if is_user_in_team : 

      for member in doc_team :
        if member['email'] == user_email : 
          user_from_team = member
      
      if user_from_team['roles'] and level in user_from_team['roles']: 
        is_user_authorized_in_team = True

  else : 
    user_from_team = { 'roles' : ['read', 'edit', 'delete', 'manage', 'comment'] }


  is_authorized = {
    'auth' : is_user_owner or is_user_authorized_in_team,
    'user_roles' : user_from_team['roles'],
    'is_owner' : is_user_owner,
  }

  return is_authorized


### - - - - - - - - - - - - - - - - - - - - - - - ### 
### INDEX LEVEL
### - - - - - - - - - - - - - - - - - - - - - - - ### 

### TO DO 
def check_index(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  user: dict = None
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


### TO DO 
def create_index_check(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  index_params: dict = None,
  user: dict = None
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


### TO DO 
def update_index_check(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  index_params: dict = None,
  user: dict = None
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




### - - - - - - - - - - - - - - - - - - - - - - - ### 
### UTILS
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def generate_new_id( 
  format = 'hex' 
  ):

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



### - - - - - - - - - - - - - - - - - - - - - - - ### 
### GENERIC REQUESTS
### - - - - - - - - - - - - - - - - - - - - - - - ### 

def view_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  query_params: dict = {},
  user: dict = None,
  ):
  """ get a document from ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }
  res = {}

  q_version = query_params.get('version', 'last')

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
  user: dict = None,
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
  user: dict = None,
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


### TO DO 
def create_version_document(
  index_name: str = None,
  doc_type: str = None,
  doc_uuid: str = None,
  params: dict = None,
  version: int = None,
  body = None,
  user: dict = None,
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
  params: dict = {},
  body = None,
  user: dict = None,
  ):
  """ update a document in ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  full_update = params.get('full_update' , False) 

  doc_body = body 

  if ES_ENABLED :
  
    ### get original doc
    orig_res_es, orig_status_es = view_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid
    )
    log_.debug( "orig_res_es : \n%s", pformat(orig_res_es))
    log_.debug( "orig_status_es : \n%s", pformat(orig_status_es))

    ### TO DO ?
    ### compare original with doc_body
    # if full_update == False :
    #   pass


    ### update doc in ES
    res_es, status_es = update_es_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      doc_body=doc_body,
      full_update=full_update 
    )

    res = res_es
    status = status_es

    ### get updated doc in ES
    res_es_updated, status_es_updated = view_document(
      index_name=index_name,
      doc_type=doc_type,
      doc_uuid=doc_uuid,
      query_params=params,
    )
    log_.debug( "res_es_updated : \n%s", pformat(res_es_updated))
    log_.debug( "status_es_updated : \n%s", pformat(status_es_updated))

    res = res_es_updated
    status = status_es_updated



  ### TO DO INSTEAD - just insert res_es_updated doc in mongoDB
  ### update doc in MongoDB
  if MONGODB_ENABLED :

    ### TO DO 
    if ES_ENABLED : 
      pass
      # body = res_es_updated['data']
      # body["version"] = res_es_updated['doc_version']['version_n']
      # body["_id"] = f"{ doc_uuid }-v{ body['version'] }" 
      # res_mongodb, status_mongodb = add_mongodb_document(
      #   collection=doc_type,
      #   index_name=index_name,
      #   doc_type=doc_type,
      #   doc_uuid=doc_uuid,
      #   doc_body=body,
      # )

    else :
      res_mongodb, status_mongodb = update_mongodb_document(
        collection=doc_type,
        index_name=index_name,
        doc_type=doc_type,
        doc_uuid=doc_uuid,
        doc_body=doc_body,
        full_update=full_update 
      )

    #   res = res_mongodb
    #   status = status_mongodb


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status



### TO DO 
# doc_uuid_list: List[str] = None,
def update_many_document(
  index_name: str = None,
  doc_type: str = None,
  params: dict = None,
  body = None,
  user: dict = None,
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
  user: dict = None,
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
  user: dict = None,
  ):
  """ remove a document from ES / MongoDB """

  log_.debug( "function : %s", inspect.stack()[0][3] )
  log_.debug( "locals() : \n%s", pformat(locals()))

  status = { 'status_code' : 200 }
  res = {}

  if ES_ENABLED :
    res_es, status_es = remove_es_index(
      index_name=index_name,
      doc_type=doc_type,
    )
    log_.debug( "res_es : \n%s", pformat(res_es))
    res, status = res_es, status_es

  if MONGODB_ENABLED :
    res_mongodb, status_mongodb = remove_mongodb_many_documents(
      collection=doc_type,
      index_name=index_name,
      doc_type=doc_type,
    )
    log_.debug( "res_mongodb : \n%s", pformat(res_mongodb))


  log_.debug( "res : \n%s", pformat(res))
  print()
  return res, status