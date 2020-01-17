from enum import Enum
from typing import List

from pydantic import BaseModel

from core.config import ROLE_SUPERUSER


class RoleEnum(Enum):
  superuser = ROLE_SUPERUSER # superuser
  user = "user" # superuser
  anonymous = "anon" # superuser


class Roles(BaseModel):
  roles: List[ RoleEnum ]


class RoleEditEnum(Enum) : 

  read    = 'read'     ### can read doc's data
  comment = 'comment'  ### can add comments in doc
  edit    = 'edit'     ### can update doc's data
  delete  = 'delete'   ### can delete doc
  manage  = 'manage'   ### can edit doc's settings