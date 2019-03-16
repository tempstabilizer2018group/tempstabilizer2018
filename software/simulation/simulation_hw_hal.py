# -*- coding: utf-8 -*-
import sys

import portable_ticks
import config_app

# Thermisches Modell der Hardware gemaess 20180707a_simulation_grob.TSC

fCH = 2.0 # Ws/K Waermekapazität beim FET, Energie pro Kelvin
fRH = 15.0 # K/W Wärmewiderstand beim FET zur Umgebung.
fRHO = 4.0 # K/W Waermewiderstand von FET zu TO
fCO = 20.0 # Ws/K Waermekapazitaet bei TO, Teilbereich des Bleches
fRO = 30.0 # K/W Waermewiderstand von von TO zu Umgebung: Waermeverlust durch Konvektion und Strahlung

fHeatW = 1.0 # Heizleistung Vorgabe in Watt

# Die Parameter der simulierten Hardware
fDACzeroHeat_V = 1.55 # Maximale Spannung für 0W
fSupplyHV_V = 48.0 # Maximale Speisung vom FET
fR2 = 3.0	# Widerstand unter FET


# Beispiel Modell, Berechnung naechste Temperaturen
def KennliniePowerFET(fDac_V):
  """
     >>> KennliniePowerFET(-0.1)
     0.0
     >>> KennliniePowerFET(0.0)
     0.0
     >>> KennliniePowerFET(fDACzeroHeat_V-0.1)
     0.0
     >>> KennliniePowerFET(fDACzeroHeat_V)
     0.0
     >>> KennliniePowerFET(fDACzeroHeat_V+0.1)
     1.6000000000000014
     >>> KennliniePowerFET(fDACzeroHeat_V+0.2)
     3.1999999999999993
     >>> KennliniePowerFET(fDACzeroHeat_V+0.3)
     4.800000000000001
     >>> KennliniePowerFET(fDACzeroHeat_V+0.4)
     6.400000000000002
  """
  fHeat_W = (fDac_V - fDACzeroHeat_V) / fR2 * fSupplyHV_V
  fHeat_W = max(0.0, fHeat_W)
  return fHeat_W


class Hw:
  """
    Abstrahiert die Hardware.
    timeIncrement() berechnet die Temperaturen neu. Diese Methode ist NUR in der simulierten Hardware vorhanden!
    Die Hardware abstrahiert den Timer.
    Die Hardware abstrahiert fTempH und fTempO.
  """
  def __init__(self, objTagesmodell=None):
    self.listEnvironsAddressI2C = []
    self.iI2cFrequencySelected = 4711
    assert objTagesmodell != None
    self.objTagesmodell = objTagesmodell
    # Startwerte
    fTempEnvirons_C = self.messe_fTempEnvirons_C
    assert fTempEnvirons_C != None
    self.__fTempH_C = fTempEnvirons_C
    self.__fTempO_C = fTempEnvirons_C
    self.__fDac_V__ = 3.3 # V
    self.fDac_V = 0.0
    self.fHeat_W = 0.0
    self.messe_fDiskFree_MBytes = 1.5

  def isPowerOnReset(self):
    return True

  def timeIncrement(self, iDelay_ms, fDac_V):
    self.fDac_V = fDac_V
    self.fHeat_W = KennliniePowerFET(fDac_V)
    fTempEnvirons_C = self.messe_fTempEnvirons_C
    assert fTempEnvirons_C != None

    while iDelay_ms > 0:
      self._timeIncrement(fTempEnvirons_C)
      portable_ticks.objTicks.increment_ticks_ms(config_app.iTimeProcess_O_H_ms)
      iDelay_ms -= config_app.iTimeProcess_O_H_ms

  def _timeIncrement(self, fTempEnvirons_C):
    # Leistung zu H
    fHLeistungW = self.fHeat_W - (self.__fTempH_C-fTempEnvirons_C)/fRH - (self.__fTempH_C-self.__fTempO_C)/fRHO
    # Leistung zu O
    fOLeistungW = (self.__fTempH_C-self.__fTempO_C)/fRHO - (self.__fTempO_C-fTempEnvirons_C) / fRO
    fTempHnew_C = self.__fTempH_C + (fHLeistungW * config_app.iTimeProcess_O_H_ms / 1000.0 / fCH)
    fTempOnew_C = self.__fTempO_C + (fOLeistungW * config_app.iTimeProcess_O_H_ms / 1000.0 / fCO)

    self.__fTempH_C = fTempHnew_C
    self.__fTempO_C = fTempOnew_C

  def startTempMeasurement(self):
    pass

  # @property
  # def iTime_ms(self):
  #   return self.__iTime_ms

  # @iTime_ms.setter
  # def iTime_ms(self, iTime_ms):
  #   self.__iTime_ms = iTime_ms

  @property
  def messe_fTempH_C(self):
    return self.__fTempH_C

  @property
  def messe_fTempO_C(self):
    return self.__fTempO_C

  @property
  def messe_fTempEnvirons_C(self):
    portable_ticks.count('simulation_hw_hal.Hw.messe_fTempEnvirons_C')
    iTime_ms = portable_ticks.objTicks.time_ms()
    return self.objTagesmodell.get_fTemp_C(iTime_ms=iTime_ms)

  @property
  def messe_iDiskFree_MBytes(self):
    iDISK_SIZE_MBYTES = 4.0
    iDSIK_REDUCTION_PER_MS_MBYTES = 0.0000004
    # Disk is empty after 2.7h: iDISK_SIZE_MBYTES/(60.0*60.0*1000.0*iDSIK_REDUCTION_PER_MS_MBYTES)
    iTime_ms = portable_ticks.objTicks.time_ms()
    iDiskFree_Bytes = iDISK_SIZE_MBYTES - iTime_ms*iDSIK_REDUCTION_PER_MS_MBYTES
    return max(iDiskFree_Bytes, -0.1)

  @property
  def bZeroHeat(self):
    '''Returns True if ZeroHeat detected.'''
    return self.__fDac_V__ <= fDACzeroHeat_V

  @property
  def bButtonPressed(self):
    '''Returns True if the Button is pressed.'''
    return False

  @property
  def fDac_V(self):
    return self.__fDac_V__

  # Voltage between 0.0 and 3.3V
  @fDac_V.setter
  def fDac_V(self, fDac_V_param):
    self.__fDac_V__ = fDac_V_param

  def setLed(self, bOn):
    # print('setLed(%d)' % bOn)
    pass

  def toggleLed(self):
    # print('toggleLed()')
    pass

  def isPowerOnReboot(self):
    return True

  @property
  def messe_fSupplyHV_V(self):
    # We don't know the supply voltage - this may happen on old hardware.
    # We assume a high supply voltage to prevent overheat.
    return 47.11

  @property
  def messe_listTempEnvirons_C(self):
    return []

  @property
  def messe_iDiskFree_MBytes(self):
    return 47.11

  @property
  def messe_iMemFree_Bytes(self):
    return 47.11

def my_function(a, b):
  """
  >>> my_function(2, 3)
  6
  >>> my_function('a', 3)
  'aaa'
  """
  return a * b


if __name__ == "__main__":
  import doctest
  doctest.testmod()
