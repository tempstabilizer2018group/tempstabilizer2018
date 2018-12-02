# -*- coding: utf-8 -*-

strUniqueId = 'simulation'

import sys
if sys.platform == 'esp32':
  import machine
  strUniqueId = ''.join(['%02X'%i for i in machine.unique_id()])

strNode = 'simul4711'
strSite = 'pc_maerki'

if strUniqueId == '3C71BF0F97A4':
  strSerial = '2018-09-07_01'
  strNode = 'steel'
  strSite = 'hombrechtikon'

if strUniqueId == '840D8E1BC40C':
  strSerial = '2018-09-07_03'
  strNode = 'aluminium'
  strSite = 'hombrechtikon'
