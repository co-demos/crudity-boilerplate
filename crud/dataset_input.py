from log_config import log_, pformat

from core import config
from models.config import DSI_DOC_TYPE

from .utils import *

log_.debug(">>> crud/dataset_input.py")




def get_dsi(
  doc_uuid: str,
  query_params,
  ):
  """ get a dsi from ES / MongoDB """

  res = get_document(
    DSI_DOC_TYPE,
    doc_uuid,
    query_params,
  )

  return res



def search_dsis(
  query_params,
  ):
  """ get a dsi from ES / MongoDB """

  res = search_documents(
    DSI_DOC_TYPE,
    query_params,
  )

  return res



def create_dsi(
  doc_uuid: str,
  params,
  body,
  ):
  """ get a dsi from ES / MongoDB """

  res = create_document(
    DSI_DOC_TYPE,
    doc_uuid,
    params,
    body
  )

  return res



def update_dsi(
  doc_uuid: str,
  params,
  body,
  ):
  """ get a dsi from ES / MongoDB """

  res = update_document(
    DSI_DOC_TYPE,
    doc_uuid,
    params,
    body
  )

  return res



def remove_dsi(
  doc_uuid: str,
  ):
  """ get a dsi from ES / MongoDB """

  res = remove_document(
    DSI_DOC_TYPE,
    doc_uuid,
  )
  
  return res