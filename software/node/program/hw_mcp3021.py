# -*- coding: utf-8 -*-

'''
  I2C-Interface to the MCP3021 "10-Bit A/D Converter"
  http://ww1.microchip.com/downloads/en/DeviceDoc/20001805C.pdf
  Address: 0x4D (MCP3021A5T-E/OT)
'''
# MCP3021A5T-E/OT
# https://www.mouser.ch/datasheet/2/268/21805a-74229.pdf
# http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/light.inc.php
# '0x%02X' % 0b01001101 = 0x4D
# '0x%02X' % 0b11001101 = 0xCD

# A2, A1, A0
I2C_ADDRESS = 0x4D  # 1, 0, 1

MAXVALUE = 0x03FF
fMAXVALUE = float(MAXVALUE+1)

fR13_OHM = 10000000.0
fR14_OHM = 510000.0
fV_REF = 3.3
fFACTOR = fV_REF/fR14_OHM*(fR14_OHM+fR13_OHM)/fMAXVALUE

class MCP3021:
  def __init__(self, i2c):
    self.i2c = i2c

  def readV(self):
    '''
      returns HV (the supply voltage) in Volt
    '''
    return fFACTOR * self.readRaw()

  def readRaw(self):
    '''
      returns a value between 0x0000 and 0x03FF
    '''
    bValue = self.i2c.readfrom(I2C_ADDRESS, 2)
    iUpperByte = bValue[0] & 0x0F
    iLowerByte = bValue[1] & 0xFC
    iValueRaw = int(iUpperByte<<6) + int(iLowerByte>>2)
    return iValueRaw

