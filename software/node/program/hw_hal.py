# -*- coding: utf-8 -*-
import uos
import utime
import uerrno
import machine
import config_app

import hw_max30205
import hw_mcp4725
import hw_mcp3021

import portable_ticks

'''
  I2C-Adresses

  import machine
  pin_sda = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP) 
  pin_scl = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
  i2c = machine.I2C(freq=1000000, scl=pin_scl, sda=pin_sda) 
  i2c.scan()

  bin, hex, name
  72   0x90  I2C_ADDRESS_TempO
  73   0x92  I2C_ADDRESS_TempH
  79   0x9E  I2C_ADDRESS_Environs
  96   0xC0  DAC
'''
I2C_ADDRESS_TempO = hw_max30205.I2C_ADDRESS_A
I2C_ADDRESS_TempH = hw_max30205.I2C_ADDRESS_B
I2C_ADDRESS_Environs = 0x9E

# Taster
pin_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
# hv_ok
pin_hv_ok = machine.Pin(17, machine.Pin.IN)
# zero_heat
pin_zero_heat = machine.Pin(21, machine.Pin.IN)
# LED
pin_led = machine.Pin(22, machine.Pin.OUT)

# KO
pin_gpio5 = machine.Pin(5, machine.Pin.OUT)
pin_gpio18 = machine.Pin(18, machine.Pin.OUT)
pin_gpio19 = machine.Pin(19, machine.Pin.OUT)

pin_sda = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP) 
pin_scl = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

class Hw:
  def __init__(self):
    self.iTimeStart_ms = utime.ticks_ms()
    self.__objHwI2cEnvironsInterval = portable_ticks.Interval(iInterval_ms=config_app.iHwI2cEnvironsInterval_ms, bForceFirstTime=True)

    self.i2c = machine.I2C(freq=1000000, scl=pin_scl, sda=pin_sda) 
    self.listAddressI2C = self.i2c.scan()
    self.listAddressI2C = sorted(self.listAddressI2C)
    self.listEnvironsAddressI2C = hw_max30205.filterEnvironsI2C(self.listAddressI2C)
    self.listEnvironsAddressI2C.remove(hw_mcp3021.I2C_ADDRESS)
    def listToHexString(list):
      return ','.join(map(lambda v: '0x%02X' % v, list))
    print('listAddressI2C:', listToHexString(self.listAddressI2C))
    print('listEnvironsAddressI2C:', listToHexString(self.listEnvironsAddressI2C))

    self.MAX30205 = hw_max30205.MAX30205(self.i2c)
    self.MCP4725 = hw_mcp4725.MCP4725(self.i2c)
    self.MCP3021 = None
    if hw_mcp3021.I2C_ADDRESS in self.listAddressI2C:
      self.MCP3021 = hw_mcp3021.MCP3021(self.i2c)

    self.MCP4725.config(power_down='Off' ,value=0x0000, eeprom=True)

    # Make sure, that 'self.__fHV_V' is defined
    self.messe_fHV_V

  def startTempMeasurement(self):
    self.MAX30205.oneShotNormalA(I2C_ADDRESS_TempH)
    self.MAX30205.oneShotNormalA(I2C_ADDRESS_TempO)

  @property
  def cached_fHV_V(self):
    return self.__fHV_V

  @property
  def messe_fHV_V(self):
    self.__fHV_V = self.__messe_fHV_V()
    return self.__fHV_V

  def __messe_fHV_V(self):
    if self.MCP3021 != None:
      return self.MCP3021.readV()
    return 20.01
    '''
    try:
      return self.MCP3021.readV()
    except OSError as osError:
      if osError.args[0] == uerrno.ENODEV:
        return 20.01
      raise
    '''

  @property
  def messe_fTempH_C(self):
    return self.MAX30205.oneShotNormalB(I2C_ADDRESS_TempH)

  @property
  def messe_fTempO_C(self):
    return self.MAX30205.oneShotNormalB(I2C_ADDRESS_TempO)

  @property
  def messe_listTempEnvirons_C(self):
    map(self.MAX30205.oneShotNormalA, self.listEnvironsAddressI2C)
    listTempEnvirons_C = list(map(self.MAX30205.oneShotNormalB, self.listEnvironsAddressI2C))
    return listTempEnvirons_C

  @property
  def messe_iDiskFree_MBytes(self):
    l = uos.statvfs('/')
    free_bytes = l[0]*l[3]
    return free_bytes/1000000.0

  @property
  def bZeroHeat(self):
    '''Returns True if ZeroHeat detected.'''
    return pin_zero_heat.value() == 1

  @property
  def bButtonPressed(self):
    '''Returns True if the Button is pressed.'''
    return pin_button.value() == 0

  @property
  def fDac_V(self):
    return self.__fDac_V__

  # Voltage between 0.0 and 3.3V
  @fDac_V.setter
  def fDac_V(self, fDac_V_param):
    self.__fDac_V__ = fDac_V_param
    iDac = int(fDac_V_param * 0x0FFF / 3.3)
    iDac = min(0x0FFF, max(0, iDac))
    self.MCP4725.write(iDac)

  def setLed(self, bOn):
    pin_led.value(bOn)

  def toggleLed(self):
    portable_ticks.count('hw_hal.toggleLed()')
    pin_led.value(not pin_led.value())

def setTempOS():
  hw = Hw()
  print('fTempH: %03f %03f' % (hw.messe_fTempH_C, hw.messe_fTempO_C))

  fTempOS_C, fTempHyst_C = hw.MAX30205.getTempOS(hw_max30205.I2C_ADDRESS_B)
  print('fTempOS/fTempHyst: %03f %03f' % (fTempOS_C, fTempHyst_C))

  # hw.MAX30205.setTempOS(hw_max30205.I2C_ADDRESS_B, 35.0, 34.5)
  hw.MAX30205.setTempOS(hw_max30205.I2C_ADDRESS_B, 40.0, 39.5)

  fTempOS_C, fTempHyst_C = hw.MAX30205.getTempOS(hw_max30205.I2C_ADDRESS_B)
  print('fTempOS/fTempHyst: %03f %03f' % (fTempOS_C, fTempHyst_C))
