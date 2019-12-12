from log_config import log_, pformat

import uuid
from core import config

from db.database_es import *
from db.database_mongodb import *

log_.debug(">>> crud/utils.py")




def generate_new_id():
  return str( uuid.uuid4() )



def get_document(
  doc_type: str,
  doc_uuid: str,
  query_params,
  ):
  """ get a document from ES / MongoDB """

  return



def search_documents(
  doc_type: str,
  query_params,
  ):
  """ search a document from ES / MongoDB """

  return



def create_document(
  doc_type: str,
  params,
  body,
  ):
  """ create a document in ES / MongoDB """

  return



def create_version_document(
  doc_type: str,
  doc_uuid: str,
  params,
  body,
  ):
  """ create a version document in MongoDB """

  return



def update_document(
  doc_type: str,
  doc_uuid: str,
  params,
  body,
  ):
  """ update a document in ES / MongoDB """

  return 



def remove_document(
  doc_type: str,
  doc_uuid: str,
  ):
  """ remove a document from ES / MongoDB """

  return 
