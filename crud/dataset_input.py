from log_config import log_, pformat
import inspect

from core import config
from models.config import DSI_DOC_TYPE, DSR_DOC_TYPE

from .utils import *

print()
log_.debug(">>> crud/dataset_input.py")





def view_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  ):
  """ get a dsi from ES / MongoDB """

  res, status = view_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    query_params = query_params,
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def search_dsis(
  query_params: dict = None,
  ):
  """ search dsi(s) from ES / MongoDB """

  res, status = search_documents(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    query_params = query_params,
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def create_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ create a dsi in ES / MongoDB """

  log_.debug("body : \n%s", pformat(body) )

  ### create index if not existing
  index, status_index = create_index_check(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    index_params = query_params,
  )

  ### create metadata doc
  res, status = create_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
    body = body
  )

  ### loop if necessary to create dmt | dmf 



  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def update_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ update a dsi from ES / MongoDB """

  ### check if DSI exists first 

  ### update DSR document
  res, status = update_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
    body = body
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def remove_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  ):
  """ remove a dsi from ES / MongoDB """

  ### remove DSI doc
  res, status = remove_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
  )
  
  ### remove corresponding DSRs docs 
  res_dsr, status_dsr = remove_many_documents(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    params = query_params,
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status