from enum import Enum, IntEnum


class OpenDataLevelEnum(str, Enum) : 
  opendata = 'opendata'
  commons = 'commons'
  team = 'team'
  private = 'private'

class LicenceEnum(str, Enum) : 
  MIT = 'MIT'
  OBDL = 'OBDL'