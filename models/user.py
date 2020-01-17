from typing import List, Optional, Union
from datetime import date, datetime, time, timedelta

from pydantic import BaseModel

from models.config import USERPROFILE_DOC_TYPE
from models.datalog import DataLogBase, Comment
from models.role import RoleEnum, RoleEditEnum


class UserLogin(BaseModel):

  email: str
  password: str

  class Config:
    schema_extra = {
      'example': {
        "email": "ostrom@emailna.co",
        "password": "a-very-common-password",
      },
    }


class TeamMember(BaseModel):
  
  email: str
  roles: List[ Union[str, RoleEditEnum] ] = [ RoleEditEnum.read ]
  comments: Optional[ List[ Comment ] ] = []

  # user_id: Optional[ str ] = None 

  # disabled: Optional[ bool ] = False

  class Config:

    schema_extra = {

      'example': {
        "email": "test@email.com",
        "roles": [ 
          "read", 
          "comment", 
          "edit", 
          "delete", 
          "manage"
        ],
        "comments" : [
          {
            'text' : "a test user who can do anything on this document",
            'created_by' : "test@email.com",
            'created_at' : datetime.now()
          }
        ]
      },

    }

class TeamMemberIn(TeamMember):
  
  added_at: datetime = None
  added_by: str = None







class UserBase(BaseModel):
  email: Optional[str] = None
  admin_roles: Optional[ List[Union[str, RoleEnum]] ] = None
  admin_channels: Optional[ List[Union[str, RoleEnum]] ] = None
  disabled: Optional[bool] = None


# Shared properties in DB
class UserBaseInDB(UserBase):
  username: Optional[str] = None
  full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
  username: str
  email: str
  password: str
  admin_roles: List[Union[str, RoleEnum]] = []
  admin_channels: List[Union[str, RoleEnum]] = []
  disabled: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
  password: Optional[str] = None


# Additional properties to return via API
class User(UserBaseInDB):
  pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
  type: str = USERPROFILE_DOC_TYPE
  hashed_password: str
  username: str


# Additional properties in Sync Gateway
class UserSyncIn(UserBase):
  name: str
  password: Optional[str] = None
