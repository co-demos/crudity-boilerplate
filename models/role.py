from enum import Enum
from typing import List

from pydantic import BaseModel

from core.config import ROLE_SUPERUSER


class RoleEnum(Enum):
  superuser = ROLE_SUPERUSER # superuser
  user = "user" # superuser
  anonymous = "anon" # superuser


class Roles(BaseModel):
  roles: List[RoleEnum]
