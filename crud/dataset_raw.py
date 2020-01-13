from log_config import log_, pformat
import inspect 

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

  res, status = view_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    query_params = query_params,
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def search_dsrs(
  dsi_uuid: str = None,
  query_params: dict = None,
  ):
  """ search dsr(s) from ES / MongoDB """

  res, status = search_documents(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    query_params = query_params,
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def create_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ create a dsr in ES / MongoDB """

  ### check if DSI exists first 

  ### add document
  res, status = create_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    params = query_params,
    body = body
  )

  log_.debug( "status : \n%s", pformat(status))
  log_.debug( "res : \n%s", pformat(res))

  return res, status



def update_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  body = None,
  ):
  """ update a dsr from ES / MongoDB """

  ### check if DSR exists first 

  ### update DSR document
  res_update, status_update = update_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    params = query_params,
    body = {
      'data' : { **body.update_data },
      'modified_at' : body.modified_at,
      'modified_by' : body.modified_by
    }
  )

  ### retrieve full updated doc
  res, status = view_document(
    index_name = dsi_uuid,
    doc_type = DSR_DOC_TYPE,
    doc_uuid = dsr_uuid,
    query_params = {
      **query_params,
      'version' : 'last'
    },
  )

  # log_.debug( "res : \n%s", pformat(res))
  # log_.debug( "status : \n%s", pformat(status))

  return res, status



def remove_dsr(
  dsi_uuid: str = None,
  dsr_uuid: str = None,
  query_params: dict = None,
  ):
  """ remove a dsr from ES / MongoDB """

  ### get dsr infos
  res_dsr, status_dsr = view_dsr(
    dsi_uuid = dsi_uuid,
    dsr_uuid = dsr_uuid,
    query_params = query_params
  )
  log_.debug( "res_dsr : \n%s", pformat(res_dsr))



  if query_params['full_remove'] == True : 

    ### remove corresponding DSR doc
    res, status = remove_document(
      index_name = dsi_uuid,
      doc_type = DSR_DOC_TYPE,
      doc_uuid = dsr_uuid,
      params = query_params,
    )
  
  else : 

    ### update corresponding DSR doc as 'deleted'
    res, status = update_document(
      index_name = dsi_uuid,
      doc_type = DSR_DOC_TYPE,
      doc_uuid = dsr_uuid,
      params = query_params,
      body = { 'is_deleted' : True }
    )

  log_.debug( "res : \n%s", pformat(res))
  log_.debug( "status : \n%s", pformat(status))

  return res, status