# -*- coding: utf-8 -*-

'''
  I2C-Interface to the MAX30205 "Human Body Temperature Sensor"
  https://datasheets.maximintegrated.com/en/ds/MAX30205.pdf
  Addressrange: 0x80 - 0xBE
'''
import array
import portable_ticks

# NOTE: In the datasheet, the address is multiplied by 2. For example 0x48 is 0x90 in the datasheet.

# A2, A1, A0
I2C_ADDRESS_A = 0x48 # 0x90  # 0, 0, 0
I2C_ADDRESS_B = 0x49 # 0x92  # 0, 0, 1

I2C_ADDRESS_MIN = 0x40 # 0x80
I2C_ADDRESS_MAX = 0x5F # 0xBE

def filterEnvironsI2C(listDevicesI2C, I2C_ADDRESS_converterAD):
  '''
    Selects all devices from the list which measure environment tempertatures
  '''

  def isEnvironI2C(iI2C):
    '''
      returns true if this i2c-address is to measure environment tempertatures
    '''
    if iI2C < I2C_ADDRESS_MIN:
      return False
    if iI2C > I2C_ADDRESS_MAX:
      return False
    if iI2C in (I2C_ADDRESS_A, I2C_ADDRESS_B, I2C_ADDRESS_converterAD):
      # These sensors measure TempO_C and Temp_H_c
      return False
    return True

  return list(filter(isEnvironI2C, listDevicesI2C))

REG_TEMP = 0b00000000
REG_CONFIG = 0b00000001
REG_T_HYST = 0b00000010
REG_T_OS = 0b00000011

REG_CONFIG_ONESHOT = 0b10000000
REG_CONFIG_TIMEOUT = 0b01000000
REG_CONFIG_DATAFORMAT = 0b00100000
REG_CONFIG_FAULTQUEUE = 0b00011000
REG_CONFIG_OSPOLARITY = 0b00000100
REG_CONFIG_COMPARATOR = 0b00000010
REG_CONFIG_SHUTDOWN = 0b00000001

TEMP_0C = 0x0000
TEMP_64C = 0x4000

CONVERSION_TIME_MS = 50

class MAX30205:
  def __init__(self, i2c):
    self.i2c = i2c

  def setTempOS(self, i2cAddress, fTempOS_C, fTempHyst_C):
    '''
      Set TempOS and TempHyst
      Raising above Temp OS, the thermostat opens
      Lowering below Temp Hyst, the thermostat closes
    '''

    def write(iRegister, fTemp):
      iTemp = int(fTemp*TEMP_64C/64.0)
      iTempMSB = (iTemp>>8)&0xFF
      iTempLSB = iTemp&0xFF
      self.i2c.writeto_mem(i2cAddress, iRegister, array.array('b', (iTempMSB, iTempLSB)))

    write(REG_T_OS, fTempOS_C)
    write(REG_T_HYST, fTempHyst_C)

  def getTempOS(self, i2cAddress):
    '''
      Read TempOS and TempHyst from the chip
    '''
    fTempOS_C = self.__readTemp(i2cAddress, REG_T_OS)
    fTempHyst_C = self.__readTemp(i2cAddress, REG_T_HYST)

    return fTempOS_C, fTempHyst_C

  def __readTemp(self, i2cAddress, iRegister):
    '''
      read temperature (2 bytes)
    '''
    bTemp = self.i2c.readfrom_mem(i2cAddress, iRegister, 2)
    iTemp = int((bTemp[0]<<8) | bTemp[1])
    fTemp = iTemp*64.0/TEMP_64C
    return fTemp

  def oneShotNormalA(self, i2cAddress):
    '''
      Start Oneshot and Shutdown afterwards
    '''
    self.i2c.writeto_mem(i2cAddress, REG_CONFIG, array.array('b', (REG_CONFIG_ONESHOT|REG_CONFIG_SHUTDOWN,)))

  def oneShotNormalB(self, i2cAddress):
    fTemp = self.__readTemp(i2cAddress, REG_TEMP)
    return fTemp

  def oneShotNormal(self, i2cAddress):
    self.oneShotNormalA(i2cAddress)
    portable_ticks.delay_ms(CONVERSION_TIME_MS)
    return self.oneShotNormalB(i2cAddress)

