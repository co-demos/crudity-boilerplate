from log_config import log_, pformat
import inspect

from core import config
from models.config import DSI_DOC_TYPE, DSR_DOC_TYPE
from models.auth import *

from .utils import *

print()
log_.debug(">>> crud/dataset_input.py")





def view_dsi(
  dsi_uuid: str = None,
  query_params: dict = {},
  user: dict = {},
  ):
  """ get a dsi from ES / MongoDB """

  ### TO DO 
  ### check user's auth 
  
  res_dsi, status_dsi = view_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    query_params = query_params,
    user = user,
  )
  # log_.debug( "res_dsi : \n%s", pformat(res_dsi))
  # log_.debug( "status_dsi : \n%s", pformat(status_dsi))

  ### TO DO 
  ### check user's auth 

  has_user_auth = is_user_authorized(
    user = user,
    doc_auth = DocAuthData(**res_dsi['_source']),
    level = 'read',
  )
    # level = level,
  log_.debug( "has_user_auth : \n%s", pformat(has_user_auth))


  return res_dsi, status_dsi



def search_dsis(
  query_params: dict = None,
  user: dict = None
  ):
  """ search dsi(s) from ES / MongoDB """

  ### TO DO 
  ### check user's auth 

  res, status = search_documents(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    query_params = query_params,
    user = user
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def create_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  body = None,
  user: dict = None
  ):
  """ create a dsi in ES / MongoDB """

  log_.debug("body : \n%s", pformat(body) )

  ### create index if not existing
  index, status_index = create_index_check(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    index_params = query_params,
    user = user,
  )

  ### create metadata doc
  res, status = create_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
    body = body,
    user = user,
  )

  ### TO DO 
  ### loop if necessary to create dmt | dmf 



  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def update_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  body = None,
  user: dict = None,
  level: str = 'edit',
  ):
  """ update a dsi from ES / MongoDB """

  ### check if DSI exists first 

  ### get corresponding DSI
  res_dsi, status_dsi = view_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    user = user,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### TO DO 
  ### check user's auth 
  has_user_auth = is_user_authorized(
    user = user,
    doc_auth = DocAuthData(**res_dsi['_source']),
    level = level
  )
  log_.debug( "has_user_auth : \n%s", pformat(has_user_auth))



  ### update DSI document
  res_update, status_update = update_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
    body = body,
    # body = {
    #   **body.update_data,
    #   'modified_at' : body.modified_at,
    #   'modified_by' : body.modified_by,
    # },
    user = user
  )
  # log_.debug( "res_update : \n%s", pformat(res_update))
  # log_.debug( "status_update : \n%s", pformat(status_update))


  ### retrieve full updated doc
  # res, status = view_document(
  #   index_name = DSI_DOC_TYPE,
  #   doc_type = 'metadata',
  #   doc_uuid = dsi_uuid,
  #   query_params = {
  #     **query_params,
  #     'version' : 'last'
  #   },
  # )
  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res_update, status_update
  # return res, status



def remove_dsi(
  dsi_uuid: str = None,
  query_params: dict = {},
  user: dict = {}
  ):
  """ remove a dsi from ES / MongoDB """

  ### get corresponding DSI

  res_dsi, status_dsi = view_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    user = user,
  )
  log_.debug( "res_dsi : \n%s", pformat(res_dsi))

  ### TO DO 
  ### check user's auth 
  has_user_auth = is_user_authorized(
    user = user,
    doc_auth = DocAuthData(**res_dsi['_source']),
    level = 'delete'
  )
  log_.debug( "has_user_auth : \n%s", pformat(has_user_auth))



  ### remove data
  if query_params['full_remove'] == True : 

    ### remove DSI doc
    res, status = remove_document(
      index_name = DSI_DOC_TYPE,
      doc_type = 'metadata',
      doc_uuid = dsi_uuid,
      params = query_params,
      user = user,
    )
    
    print("- - "*40)
    
    ### remove corresponding DSRs docs 
    res_dsr, status_dsr = remove_many_documents(
      index_name = dsi_uuid,
      doc_type = DSR_DOC_TYPE,
      params = query_params,
      user = user
    )

  else : 
    ### update DSI doc as 'deleted'
    res, status = update_document(
      index_name = DSI_DOC_TYPE,
      doc_type = 'metadata',
      doc_uuid = dsi_uuid,
      params = query_params,
      body = { 'is_deleted' : True },
      user = user
    )

    ### update corresponding DSR docs as 'deleted'
    ### TO DO 
    ### update DSI's DSR docs as 'deleted'
    # res, status = update_many_document(
    #   index_name = dsi_uuid,
    #   doc_type = DSR_DOC_TYPE,
    #   # doc_uuid_list = [ dsi_uuid ],
    #   params = query_params,
    #   body = { 'is_deleted' : True }
    # )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status