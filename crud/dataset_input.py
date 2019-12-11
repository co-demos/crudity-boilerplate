from log_config import log_, pformat

from core import config
from models.config import DSI_DOC_TYPE

from . import utils


log_.debug(">>> crud/dataset_input.py")

from db.database_es import es 
from db.database_mongodb import *


def get_doc_uuid(uuid: str):
  return f"{DSI_DOC_TYPE}::{uuid}"