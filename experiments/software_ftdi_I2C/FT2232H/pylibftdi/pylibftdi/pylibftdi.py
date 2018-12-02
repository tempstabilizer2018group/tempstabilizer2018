# -*- coding: utf-8 -*-

import pylibftdi

with pylibftdi.Device() as i2c:
  i2c.baudrate = 100000