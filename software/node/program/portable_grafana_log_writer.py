# -*- coding: utf-8 -*-
import os

import portable_grafana_datatypes
from portable_grafana_datatypes import INFLUXDB_TAG_NODE
from portable_grafana_datatypes import INFLUXDB_TAG_ENVIRONS
import portable_ticks
import config_app

def nextFilename(strFilenameTemplate='test_hw_pidh_pido_day_log_%02d.txt'):
  listFiles = os.listdir()
  for i in range(100):
    strFilename = strFilenameTemplate % i
    if strFilename in listFiles:
      continue
    print('strFilename: %s' % strFilename)
    return strFilename
  raise Exception('nextFilename()')

class CachedLog:
  def __init__(self, strFilename):
    self.strFilename = strFilename
    self.listBuf = []

  def write(self, strMessage):
    self.listBuf.append(strMessage)
    if len(self.listBuf) < 20:
      return
    self.__flush()

  def __flush(self):
    print('flush()', self.strFilename)
    with open(self.strFilename, 'a') as fLog:
      for strLine in self.listBuf:
        fLog.write(strLine)
    self.listBuf = []

  def close(self):
    self.__flush()

class GrafanaProtocol:
  def __init__(self, listAddressI2C):
    self.__objLog = None
    self.__iLastTicks_ms = portable_ticks.objTicks.ticks_ms()
    self.__iCounter = -1
    self.__objInterval = portable_ticks.Interval(iInterval_ms=config_app.iGrafanaLogInterval_ms)

    # Temperatures will be named 'r', 's', 't', ...
    iChar = ord('r')
    self.__listGrafanaValueTempEnvirons = []
    for iAddressI2C in listAddressI2C:
      objVal = portable_grafana_datatypes.GrafanaValueFloatAvg(INFLUXDB_TAG_ENVIRONS, chr(iChar), '%02X' % iAddressI2C, 1000.0)
      self.__listGrafanaValueTempEnvirons.append(objVal)
      iChar += 1

    self.__objGrafanaValue_TempO = portable_grafana_datatypes.GrafanaValueFloatAvg(INFLUXDB_TAG_NODE, 'O', 'fTempO_C', 1000.0)
    self.__objGrafanaValue_TempO_Setpoint = portable_grafana_datatypes.GrafanaValueFloat(INFLUXDB_TAG_NODE, 'S', 'fTempO_Setpoint_C', 1000.0)
    self.__objGrafanaValue_Heat = portable_grafana_datatypes.GrafanaValueFloatAvg(INFLUXDB_TAG_NODE, 'H', 'fHeat_W', 100.0)
    self.__objGrafanaValue_PidH_bLimitHigh = portable_grafana_datatypes.GrafanaValueBoolTrue(INFLUXDB_TAG_NODE, 'L', 'PidH_bLimitHigh')
    self.__objGrafanaValue_DACzeroHeat = portable_grafana_datatypes.GrafanaValueFloatAvg(INFLUXDB_TAG_NODE, 'z', 'fDACzeroHeat_V', 1000.0)
    self.__objGrafanaValue_SupplyVoltage = portable_grafana_datatypes.GrafanaValueFloat(INFLUXDB_TAG_NODE, 'U', 'fSupplyVoltage_V', 10.0)
    self.__objGrafanaValue_DiskFree = portable_grafana_datatypes.GrafanaValueFloat(INFLUXDB_TAG_NODE, 'F', 'fDiskFree_MBytes', 100.0)

  def writeHeader(self, iI2cFrequencySelected):
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_VERSION, '1.0')
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_MAC, config_app.strMAC)
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_MAXTICK_MS, portable_ticks.objTicks.iMaxTicks_ms)
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_I2C_FREQUENCY_SELECTED_HZ, iI2cFrequencySelected)

    def logAuxiliary(objGrafanaValue, iModuloPull):
      self.logLine(portable_grafana_datatypes.TAG_GRAFANA_DATATYPE, objGrafanaValue.getConstructor())
      if config_app.bGrafanaSkipEqualValues:
        self.logLine(portable_grafana_datatypes.TAG_GRAFANA_MESSINTERVAL_MS, '%s %d' % (objGrafanaValue.strTag, iModuloPull*config_app.iGrafanaLogInterval_ms))

    logAuxiliary(self.__objGrafanaValue_TempO, config_app.iMODULO_GRAFANALOG_MEDIUM_PULL)
    logAuxiliary(self.__objGrafanaValue_TempO_Setpoint, config_app.iMODULO_GRAFANALOG_MEDIUM_PULL)
    logAuxiliary(self.__objGrafanaValue_Heat, config_app.iMODULO_GRAFANALOG_MEDIUM_PULL)
    logAuxiliary(self.__objGrafanaValue_PidH_bLimitHigh, config_app.iMODULO_GRAFANALOG_MEDIUM_PULL)
    logAuxiliary(self.__objGrafanaValue_DACzeroHeat, config_app.iMODULO_GRAFANALOG_MEDIUM_PULL)
    logAuxiliary(self.__objGrafanaValue_SupplyVoltage, config_app.iMODULO_GRAFANALOG_MEDIUM_PULL)
    logAuxiliary(self.__objGrafanaValue_DiskFree, config_app.iMODULO_GRAFANALOG_SLOW_PULL)

    for objGrafanaValue in self.__listGrafanaValueTempEnvirons:
      logAuxiliary(objGrafanaValue, config_app.iMODULO_GRAFANALOG_SLOW_PULL)

  def attachFile(self, objLog):
    assert self.__objLog == None, 'There is already a file attached!'
    self.__objLog = objLog

  def close(self):
    self.__objLog.close()
    self.__objLog = None

  def logInfo(self, strWarning):
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_INFO, strWarning)

  def logWarning(self, strWarning):
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_WARNING, strWarning)

  def logError(self, strWarning):
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_ERROR, strWarning)

  def logNtpTime(self, iSecondsSince1970_UnixEpoch):
    self.logLine(portable_grafana_datatypes.TAG_GRAFANA_NTP, str(int(iSecondsSince1970_UnixEpoch)))

  def logLine(self, strTag, strPayload):
    iTicksNow_ms = portable_ticks.objTicks.ticks_ms()
    iTicksDiff_ms = portable_ticks.objTicks.ticks_diff(iTicksNow_ms, self.__iLastTicks_ms)
    self.__objLog.write('%d %s %s\n' % (iTicksDiff_ms, strTag, strPayload))
    self.__iLastTicks_ms = iTicksNow_ms

  def __logLine(self, iEffectiveIntervalDuration_ms, strTag, strPayload):
    self.__objLog.write('%d %s %s\n' % (iEffectiveIntervalDuration_ms, strTag, strPayload))

  def logTempstablilizer(self, objTs, objHw):
    bIntervalOver, iEffectiveIntervalDuration_ms = self.__objInterval.isIntervalOver()
    if not bIntervalOver:
      return

    self.__iCounter += 1

    if (self.__iCounter % config_app.iMODULO_GRAFANALOG_MEDIUM_PUSH) == 0:
      # TODO: We could push TempO every time when it was measured. This would give a much better resolution
      self.__objGrafanaValue_TempO.pushValue(objTs.fTempO_C)
      self.__objGrafanaValue_Heat.pushValue(objTs.fHeat_W)
      self.__objGrafanaValue_PidH_bLimitHigh.pushValue(objTs.bFetMax_W_Limit_High)
      self.__objGrafanaValue_DACzeroHeat.pushValue(objTs.fDACzeroHeat_V)

    listValues = []

    def pullValue(objGrafanaValue):
      strValue = objGrafanaValue.pullValue()
      if strValue != None:
        listValues.append(objGrafanaValue.strTag + strValue)
      else:
        if not config_app.bGrafanaSkipEqualValues:
          # Einfluss von 'Leer'zeichen: 2'092 Bytes mit. 1'457 Bytes ohne.
          # Stellen für die Temperatur: Drei Stellen: 1'457 Bytes, Zwei Stellen: 997 Bytes
          listValues.append(objGrafanaValue.strTag)

    if (self.__iCounter % config_app.iMODULO_GRAFANALOG_MEDIUM_PULL) == 0:
      pullValue(self.__objGrafanaValue_TempO)
      pullValue(self.__objGrafanaValue_Heat)
      pullValue(self.__objGrafanaValue_PidH_bLimitHigh)
      pullValue(self.__objGrafanaValue_DACzeroHeat)

      # self.__objGrafanaValue_TempO_Setpoint is not AVG. So we only need to pushValue() once per pullValue()
      fSupplyHV_V = objHw.messe_fSupplyHV_V
      self.__objGrafanaValue_SupplyVoltage.pushValue(fSupplyHV_V)
      pullValue(self.__objGrafanaValue_SupplyVoltage)

      # self.__objGrafanaValue_TempO_Setpoint is not AVG. So we only need to pushValue() once per pullValue()
      self.__objGrafanaValue_TempO_Setpoint.pushValue(objTs.fTempO_Setpoint_C)
      pullValue(self.__objGrafanaValue_TempO_Setpoint)

    if (self.__iCounter % config_app.iMODULO_GRAFANALOG_SLOW_PUSH) == 0:
      listTempEnvirons_C = objHw.messe_listTempEnvirons_C
      assert len(listTempEnvirons_C) == len(self.__listGrafanaValueTempEnvirons)
      for fTempEnvirons_C, objGrafanaValueTempEnviron_C in zip(listTempEnvirons_C, self.__listGrafanaValueTempEnvirons):
        objGrafanaValueTempEnviron_C.pushValue(fTempEnvirons_C)

    if (self.__iCounter % config_app.iMODULO_GRAFANALOG_SLOW_PULL) == 0:
      for objGrafanaValueTempEnviron_C in self.__listGrafanaValueTempEnvirons:
        pullValue(objGrafanaValueTempEnviron_C)
  
      # self.__objGrafanaValue_DiskFree is not AVG. So we only need to pushValue() once per pullValue()
      iDiskFree_MBytes = objHw.messe_iDiskFree_MBytes
      self.__objGrafanaValue_DiskFree.pushValue(iDiskFree_MBytes)
      pullValue(self.__objGrafanaValue_DiskFree)

    if len(listValues) > 0:
      self.logLine(portable_grafana_datatypes.TAG_GRAFANA_VALUE, ''.join(listValues))

if __name__ == '__main__':
  objFloat = portable_grafana_datatypes.GrafanaValueFloat('S', 'fTempO_Setpoint_C', 1000.0)
  listFloatInput = (1.0, 1.0, 1.1, 1.1, 1.1, 20.0)
