import sys

# It would be good to use the constants in 'config_app'.
# However, we don't know yet 'config_app'!.
# config_app.DIRECTORY_CONFIG
sys.path.append('config')
# config_app.DIRECTORY_PROGRAM
sys.path.append('program')

from upysh import *

from hw_update_ota import Command

def _delete():
  import uos
  from portable_firmware_constants import strFILENAME_VERSION
  uos.remove(strFILENAME_VERSION)
  import machine
  machine.reset()

deleteVERSION_TXT = Command(_delete)

import hw_test_pidh_pido_day
# import hw_test_pidh_pido
# import hw_test_pidh
