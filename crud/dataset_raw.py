from log_config import log_, pformat

from core import config
from models.config import DSR_DOC_TYPE

from .utils import *

log_.debug(">>> crud/dataset_raw.py")



def get_dsr(
  doc_uuid: str,
  query_params,
  ):
  """ get a dsr from ES / MongoDB """

  res = get_document(
    DSR_DOC_TYPE,
    doc_uuid,
    query_params,
  )

  return res



def search_dsrs(
  query_params,
  ):
  """ get a dsr from ES / MongoDB """

  res = search_documents(
    DSR_DOC_TYPE,
    query_params,
  )

  return res



def create_dsr(
  doc_uuid: str,
  query_params,
  body,
  ):
  """ get a dsr from ES / MongoDB """

  res = create_document(
    DSR_DOC_TYPE,
    doc_uuid,
    query_params,
  )

  return res



def update_dsr(
  doc_uuid: str,
  query_params,
  body,
  ):
  """ get a dsr from ES / MongoDB """

  res = update_document(
    DSR_DOC_TYPE,
    doc_uuid,
    query_params,
  )

  return res



def remove_dsr(
  doc_uuid: str,
  ):
  """ get a dsr from ES / MongoDB """

  res = remove_document(
    DSR_DOC_TYPE,
    doc_uuid,
  )
  
  return res