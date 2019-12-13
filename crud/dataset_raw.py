from log_config import log_, pformat

from core import config
from models.config import DSR_DOC_TYPE

from .utils import *

print()
log_.debug(">>> crud/dataset_raw.py")



def view_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  ):
  """ get a dsr from ES / MongoDB """

  res = view_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    query_params = query_params,
  )

  return res



def search_dsrs(
  dsi_uuid: str = None,
  query_params: dict = None,
  ):
  """ search dsr(s) from ES / MongoDB """

  res = search_documents(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    query_params = query_params,
  )

  return res



def create_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ create a dsr in ES / MongoDB """

  ### check if DSI exists first 

  ### add document
  res = create_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    params = query_params,
    body = body
  )

  return res



def update_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ update a dsr from ES / MongoDB """

  ### check if DSR exists first 

  ### update DSR document
  res = update_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    params = query_params,
  )

  return res



def remove_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  ):
  """ remove a dsr from ES / MongoDB """

  res = remove_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    params = query_params,
  )
  
  return res