# -*- coding: utf-8 -*-
import math

import portable_ticks
import portable_constants

# DayMaxEstimator
# 6 Minutes
TIME_PROCESS_DAYMAXESTIMATOR_MS = 6*portable_constants.MINUTE_MS
# 6 Minutes
TIME_CALC_FTEMPO_SETPOINT_MS = portable_constants.TIME_CALC_FTEMPO_SETPOINT_MS
# 3 Hours
TIME_INTERVAL_FTEMPO_SETPOINT_MS = portable_constants.TIME_INTERVAL_FTEMPO_SETPOINT_MS

# SetpointReduction
SETPOINT_CONSTANT_MS = 24 * portable_constants.HOUR_MS
# Parabel: Nach __SETPOINT_ABNAHME_MS nimmt die Temperatur um __SETPOINT_ABNAHME_C ab.
__SETPOINT_ABNAHME_MS = 24 * portable_constants.HOUR_MS
__SETPOINT_ABNAHME_C = 0.01
SETPOINT_K_MS = __SETPOINT_ABNAHME_MS/math.sqrt(__SETPOINT_ABNAHME_C)

PERSIST_SETPOINT_TEMPO_C = 'TempO_SetpointWhenSet.fTempO_C'
PERSIST_SETPOINT_TIMESINCE_MS = 'TempO_SetpointWhenSet.iTimeSince_ms'

class TempO_SetpointWhenSet:
  '''
    Persistenz:
    Gespeichert werden muss:
      - fTempO_C
      - Die Zeit, seit der fTempO_C gesetzt wurde.
        iTimeSince_ms = ticks_diff(iTicks_now_ms, iTicks_ms)
    Das File soll jede Stunde geschrieben werden.
  '''
  def __init__(self, iTicks_ms, fTempO_C, objPersist=None):
    self.iTicks_ms = iTicks_ms
    self.fTempO_C = fTempO_C
    self.__objPersist = objPersist
    if objPersist != None:
      if objPersist.loaded:
        # Restore the value from the previous run
        self.fTempO_C = objPersist.getValue(PERSIST_SETPOINT_TEMPO_C)
        iTimeSince_ms = objPersist.getValue(PERSIST_SETPOINT_TIMESINCE_MS)
        self.iTicks_ms = portable_ticks.objTicks.ticks_add(iTicks_ms, iTimeSince_ms)

  def __calculateSetpointReduction(self, iTicks_now_ms):
    iAgeParabel_ms = iTicks_now_ms - self.iTicks_ms - SETPOINT_CONSTANT_MS
    if iAgeParabel_ms < 0:
      return 0.0
    fTmp = float(iAgeParabel_ms)/SETPOINT_K_MS
    return -fTmp*fTmp

  def calculateSetpoint(self, iTicks_now_ms):
    if self.__objPersist != None:
      # Save actual value in Persist-Object
      iTimeSince_ms = portable_ticks.objTicks.ticks_diff(iTicks_now_ms, self.iTicks_ms)
      self.__objPersist.setValue(PERSIST_SETPOINT_TEMPO_C, self.fTempO_C)
      self.__objPersist.setValue(PERSIST_SETPOINT_TIMESINCE_MS, iTimeSince_ms)
    return self.fTempO_C + self.__calculateSetpointReduction(iTicks_now_ms)

  def restart(self, iTicks_ms, fTempO_C):
    self.fTempO_C = fTempO_C
    self.iTicks_ms = iTicks_ms

TEMP_LOW_C = -100.00

class TemperatureList:
  def __init__(self, fTemp_C):
    self.iDatapoints = int(TIME_INTERVAL_FTEMPO_SETPOINT_MS/TIME_CALC_FTEMPO_SETPOINT_MS)
    self.iLastDatapoint = 0
    self.listTemp_C = [fTemp_C,]*self.iDatapoints
    self.iIndexMiddle = int(self.iDatapoints/2)

  def getLowestTemperature(self, iTemp_C=TEMP_LOW_C):
    """
      Sonst: Die tiefste Temperatur
    """
    self.iLastDatapoint += 1
    if self.iLastDatapoint >= self.iDatapoints:
      self.iLastDatapoint = 0
    self.listTemp_C[self.iLastDatapoint] = iTemp_C
    # fTempLowest_C = min(self.listTemp_C)
    listTempSorted_C = sorted(self.listTemp_C)
    fTempLowest_C = listTempSorted_C[self.iIndexMiddle]
    return fTempLowest_C

class DayMaxEstimator:
  """
    Grundsätzlich werden nur die Zeitpunkte berücksichtigt, bei welchen nicht geheizt wird.
    Die Berechnung des neuen fTempO_Setpoint_C findet alle 6 Minuten (TIME_CALC_FTEMPO_SETPOINT_MS) statt.
    Es wird immer die tiefste Temperatur der letzten 3 Stunden (TIME_INTERVAL_FTEMPO_SETPOINT_MS) berücksichtigt.
    Falls diese Temperatur höher ist als der aktuelle fTempO_Setpoint_C, so wird dieser erhöht.
    Der aktuelle fTempO_Setpoint_C wird gemäss der Funktion 'calculateSetpointReduction()' reduziert.
    Falsch: Median
  """
  def __init__(self, iTicks_ms):
    self.fOutputValue = None
    self.iNextDayEstimatorTicks_ms = iTicks_ms

    if portable_ticks.objTicks.iMaxTicks_ms < TIME_PROCESS_DAYMAXESTIMATOR_MS:
      print('WARNING: DayMaxEstimator will NEVER be called: iMaxTicks_ms<TIME_PROCESS_DAYMAXESTIMATOR_MS  (%d<%d)' % (portable_ticks.objTicks.iMaxTicks_ms, TIME_PROCESS_DAYMAXESTIMATOR_MS))

  def start(self, iTicks_ms, fTempO_Sensor, objPersist=None):
    # Initial values
    self.objTempO_SetpointWhenSet = TempO_SetpointWhenSet(iTicks_ms=iTicks_ms, fTempO_C=fTempO_Sensor, objPersist=objPersist)
    self.objTemperatureList = TemperatureList(fTempO_Sensor)
    self.iStartTime_ms = iTicks_ms

  def process(self, iTicks_ms, fTempO_Sensor, bFetMin_W_Limit_Low):
    iDiffTicks_ms = portable_ticks.objTicks.ticks_diff(iTicks_ms, self.iNextDayEstimatorTicks_ms)
    if iDiffTicks_ms > 0:
      if self.fOutputValue != None:
        # Still no need to process
        return

    self.iNextDayEstimatorTicks_ms = portable_ticks.objTicks.ticks_add(iTicks_ms, TIME_PROCESS_DAYMAXESTIMATOR_MS)

    self.fOutputValue = self.__process(iTicks_ms, fTempO_Sensor, bFetMin_W_Limit_Low)

  def __process(self, iTicks_ms, fTempO_Sensor, bFetMin_W_Limit_Low):
    portable_ticks.count('DayMaxEstimator.__process()')

    iTimeDelta_ms = portable_ticks.objTicks.ticks_diff(iTicks_ms, self.iStartTime_ms)
    if iTimeDelta_ms > TIME_CALC_FTEMPO_SETPOINT_MS:
      # Alle 6 Minuten wird die Temperatur in objTemperatureList gespeichert und der Setpoint neu berechnet.
      self.iStartTime_ms = portable_ticks.objTicks.ticks_add(self.iStartTime_ms, TIME_CALC_FTEMPO_SETPOINT_MS)
      if bFetMin_W_Limit_Low:
         fTempLowest_C = self.objTemperatureList.getLowestTemperature(fTempO_Sensor)
      else:
         fTempLowest_C = self.objTemperatureList.getLowestTemperature()
      fSetpoint_C = self.objTempO_SetpointWhenSet.calculateSetpoint(iTicks_ms)
      if fTempLowest_C < fSetpoint_C:
        return fSetpoint_C
      self.objTempO_SetpointWhenSet.restart(iTicks_ms, fTempLowest_C)
      return fTempLowest_C
    return self.objTempO_SetpointWhenSet.calculateSetpoint(iTicks_ms)

