from log_config import log_, pformat

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

  res = view_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    query_params = query_params,
  )

  return res



def search_dsis(
  query_params: dict = None,
  ):
  """ search dsi(s) from ES / MongoDB """

  res = search_documents(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    query_params = query_params,
  )

  return res



def create_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ create a dsi in ES / MongoDB """

  ### check if DSI exists first 


  ### create index if not existing
  index = create_index_check(

  )


  ### create metadata doc
  res = create_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
    body = body
  )

  ### loop if necessary to create dmt | dmf 


  return res



def update_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ update a dsi from ES / MongoDB """

  ### check if DSI exists first 

  ### update DSR document
  res = update_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
    body = body
  )

  return res



def remove_dsi(
  dsi_uuid: str = None,
  query_params: dict = None,
  ):
  """ remove a dsi from ES / MongoDB """

  ### remove DSI doc
  res = remove_document(
    index_name = DSI_DOC_TYPE,
    doc_type = 'metadata',
    doc_uuid = dsi_uuid,
    params = query_params,
  )
  
  ### remove corresponding DSRs docs 
  res_dsr = remove_many_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    params = query_params,
  )

  return res