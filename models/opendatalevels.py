from enum import Enum, IntEnum


class EditLevelEnum(str, Enum) : 
  # opendata = 'opendata'
  commons = 'commons' ### any user can edit
  team = 'team'       ### owner and team members can edit
  private = 'private' ### only owner can edit

class OpenDataLevelEnum(str, Enum) : 
  opendata = 'opendata' ### anyone can read data
  commons = 'commons'   ### any user can read data
  team = 'team'         ### owner and team members can read data
  private = 'private'   ### only owner can read data

class LicenceEnum(str, Enum) : 

  ### cf : https://www.data.gouv.fr/en/licences
  ### cf : https://opensource.org/licenses
  ### cf : https://www.gnu.org/licenses/license-list.fr.html


  ### LICENCE = identifiant SPDX


  ### public data licences 
  # by the FR government
  ETALAB = 'Etalab-2.0' 
  # share as same / identical
  OBDL_1_0 = 'OBDL-1.0'


  ### code source licences 
  # permisive licences
  APACHE_2_0 = 'Apache-2.0'
  BSD_2_CLAUSE = 'BSD-2-Clause'
  BSD_3_CLAUSE = 'BSD-3-Clause'
  CECILL_B = 'CeCILL-B'
  MIT = 'MIT'

  # reciprocity licences
  CECILL_2_1 = 'CeCILL-2.1'
  CECILL_C = 'CeCILL-C'
  GPL_3_0 = 'GPL-3.0'
  LGPL_3_0 = 'LGPL-3.0'
  AGPL_3_0 = 'AGPL-3.0'
  MPL_2_0 = 'MPL-2.0' 


# class LicenceEnum(str, Enum) : 
#   MIT = 'MIT'
#   OBDL = 'OBDL'