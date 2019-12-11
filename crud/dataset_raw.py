from log_config import log_, pformat

from core import config
from models.config import DSR_DOC_TYPE

from . import utils


log_.debug(">>> crud/dataset_raw.py")


def get_doc_uuid(uuid: str):
  return f"{DSR_DOC_TYPE}::{uuid}"
